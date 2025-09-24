import Pipeline as PL
import Outils_2 as O
from Parametres import File, Dict_wave, Channel, SF, Fmin, Fmax, Fenetre
from scipy.signal import hilbert
import numpy as np
import tkinter as tk 
from matplotlib.figure import Figure
import affichage as a

class Analyse_Object:
   
    def __init__(self,file):
        self.signal_raw, self.hypnogram = PL.import_data(file)
        self.signal_sigma = PL.raw_to_sigma(self.signal_raw).astype(np.float32)
        self.signal_sigma_hilbert = np.abs(hilbert(self.signal_sigma)).astype(np.float32)
        
        self.mask = PL.detect_artefact(self.signal_sigma)
        self.nb_artefact = O.ft_count(self.mask,1)
        
        liste_event , liste_event_long, self.liste_artefact = PL.signal_to_dico_event(self.signal_sigma_hilbert,self.mask)

        self.dico_spindle = PL.classer_event(liste_event,self.hypnogram)
        self.dico_spindle_long = PL.classer_event(liste_event_long, self.hypnogram)
        self.liste_spindle_N2_N3 = self.dico_spindle["2"] + self.dico_spindle["3"]
        self.dico_hypno = PL.count_stage(self.hypnogram)

        self.spindle_index = 0

        self.figure_artefact = a.figure_artefact(self.signal_sigma,self.mask)
        self.figure_distribution = a.figure_distribution(self.signal_raw,self.dico_spindle,self.hypnogram)
        self.figure_spindle = a.figure_spindle(self.signal_raw,self.signal_sigma,self.dico_spindle,self.spindle_index,self.liste_artefact)
        self.figure_hypnogram = a.figure_hypnogram(self.hypnogram)

        self.msg_spindle = a.msg_spindle(self.dico_spindle,self.dico_hypno)
        self.msg_artefact = a.msg_artefact(self.nb_artefact,self.liste_artefact,len(self.signal_raw))
        self.msg_hypno = a.msg_hypno(self.hypnogram)
        self.msg_global = self.msg_spindle + "\n" + self.msg_artefact 
        
    def next(self,x):
        print("index = ",self.spindle_index)
        print(f"{self.spindle_index} + {x} < {len(self.liste_spindle_N2_N3)} = {self.spindle_index + x < len(self.liste_spindle_N2_N3)}")
        if self.spindle_index + x < len(self.liste_spindle_N2_N3):
            self.spindle_index += x
            print(f"donc --> index = {self.spindle_index}")
            self.figure_spindle = a.figure_spindle(self.signal_raw,self.signal_sigma,self.dico_spindle,self.spindle_index,self.liste_artefact)

    def prev(self,x):
        print("index = ",self.spindle_index)
        print(f"{self.spindle_index} + {x} > 0 = {self.spindle_index + x > 0}")
        if self.spindle_index - x > 0:
            self.spindle_index -= x
            print(f"donc --> index = {self.spindle_index}")
            self.figure_spindle = a.figure_spindle(self.signal_raw,self.signal_sigma,self.dico_spindle,self.spindle_index,self.liste_artefact)
