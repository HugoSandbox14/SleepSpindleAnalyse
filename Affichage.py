import Pipeline as PL
import Outils_2 as O
from Parametres import File, Dict_wave, Channel, SF, Fmin, Fmax, Fenetre
from scipy.signal import hilbert
import numpy as np
import tkinter as tk 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def figure_artefact(signal,mask):
        
        time = np.arange(len(signal))
        liste_x = O.mask_to_index(mask)
        liste_y = O.index_to_artefact(liste_x, signal)
        nb_artefact = O.ft_count(mask,1)

        figure = Figure(figsize = (8,6), dpi = 75)
        ax = figure.add_subplot(111)
        ax.plot(time,signal)

        ax.scatter(liste_x, liste_y, color='red', s=1, zorder=5, label='Points surlignés')

        ax.axhline(y=50, color='green', linestyle='--', linewidth=1)
        ax.axhline(y=-50, color='green', linestyle='--', linewidth=1)
        ax.set_title(f"Représentation des artefacts")
        ax.set_xlabel("Temps (Heures)")
        ax.set_ylabel("Amplitude (µV)")

        return figure

def figure_distribution(signal, event,hypno):
    dico_color = {
        "0" : "orange",
        "1" : "orange",
        "2" : "green",
        "3" : "yellow",
        "4" : "red",
        "-1" : "red",
    }
    
    figure, (ax1, ax2) = plt.subplots(2, 1, figsize = (8,6), dpi = 75)
    labels = ["Wake","N1","N2","N3","REM"]

    liste_event = O.dico_to_list(event)

    time_1 = np.arange(len(signal)) / SF / 3600
    time_2 = np.arange(len(hypno)) / 120 
    

    ax1.plot(time_2, hypno, color='blue')
    ax1.set_title("Hypnogram")
    ax1.set_xlabel("Temps (Heures)")
    ax1.set_ylabel("Stade")
    ax1.set_yticks([0,1,2,3,4])  
    ax1.set_yticklabels(labels)
    for a,b in liste_event:
        index = a//7500
        stade = hypno[index]
        ax2.axvspan(a,b,color = dico_color[str(stade)], alpha = 0.5)
        ax2.set_xlabel("Temps (Heures)")
    ax2.set_yticks([])

    return figure

def figure_spindle(signal,signal_sigma,event,index,liste_artefact):
    events_N2 = event["2"]
    events_N3 = event["3"]
    events = O.ranger(event["2"] + event["3"])
    spindle = events[index]

    if spindle in events_N2:
        stade = "N2"
    elif spindle in events_N3:
        stade = "N3"
    else:
        stade = "?"

    start, end = spindle
    
    if start - 250 <= 0:
            start = 0
    if end + 250 >= len(signal):
            end = len(signal)
    time = end - start + 500
    time_1 = np.arange(time)
    time_2 = np.arange(len(signal))


    figure, (ax1, ax2) = plt.subplots(2, 1, figsize = (8,6), dpi = 75)

    ax1.plot(time_1,signal_sigma[start - 250:end + 250])
    ax1.set_ylim(-60,60)
    ax1.axvspan(250,len(signal_sigma[start - 250:end + 250]) - 250, color = 'red', alpha = 0.3)
    ax1.set_title(f"Evenement N°{index} ({stade})")
    
    ax2.plot(time_2,signal)
    ax2.set_ylim(-400,400)
    ax2.axvline(x = start, color = 'red', linestyle = "--", linewidth = 3,alpha = 0.5)
    for x,y in liste_artefact:
        ax2.axvline(x = x, color = 'black', linestyle = "--", linewidth = 1,alpha = 0.5)
    figure.tight_layout()
    return figure

def figure_hypnogram(hypno):
        labels = ["Wake","N1","N2","N3","REM","?"]
        count, _ = O.count_stage(hypno)
        figure = Figure(figsize = (8,6), dpi = 75)

        ax = figure.add_subplot(111)
        ax.bar(labels,count)
        ax.set_title(f"Hypnogram")
        ax.set_xlabel("Temps")
        ax.set_xlabel("Stade")
        ax.set_ylabel("Temps (minutes)")

        return figure

# def get_stat(dico_event, dico_hypno):
#     keys = dico_event.keys()
#     for key in keys:
#         nb_spindle = len(dico_event[key])
#         temps_stade = dico_hypno[key]
#         if temps_stade == 0:
#             print(f"stade {key} | --> X\n")          
#         else:   
#             print(f"stade {key} --> {nb_spindle} Spindle detecté | ratio --> {round((nb_spindle/len(O.dico_to_list(dico_event))) * 100,1)}%", end = " ")
#             print(f"temps en stade --> {O.sec_to_hms(temps_stade)} | --> {round(nb_spindle/(temps_stade // 60),2)} spindle par minutes")


def msg_artefact(nb_artefact,liste_artefact,nb_point): 
    ratio_artefact = nb_artefact/nb_point * 100
    msg = f"Nombre d'artefact dans le signal {nb_artefact}\nRatio d'artefact dans le signal {round(ratio_artefact,2)}%\nNombre de spindle supprimés --> {len(liste_artefact)}"

    return msg

def msg_spindle(dico_event,dico_hypno):
    keys = ["2","3"]
    msg = ""
    for key in keys:
        x = len(dico_event[key])
        y = dico_hypno[key]
        if y == 0:
            msg += f"stade N{key} | --> X\n"          
             
        else:
            msg += f"stade N{key} | --> {x} spindles detectés | --> {O.sec_to_hms(y)} | --> {round(x/(y/60),2)} spindles par minutes\n"
    return msg 

def msg_hypno(hypno):
    msg = ""
    labels = ["Wake","N1","N2","N3","REM","?"]
    count, _ = O.count_stage(hypno)
    total = np.sum(count)
    for i in range(len(labels)):
        msg += f"temps passé en stade {labels[i]} --> {round(count[i]/total*100,2)}%\n"
    
    return msg
