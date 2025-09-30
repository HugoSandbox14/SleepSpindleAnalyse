import Pipeline as PL
import Tools as O
from Settings import File, Dict_wave, Channel, SF, Fmin, Fmax, Window
from scipy.signal import hilbert
import numpy as np
import tkinter as tk 
from matplotlib.figure import Figure
import Display as D

class Analyse_Object:
   
    def __init__(self,file):
        self.signal_raw, self.hypnogram = PL.import_data(file)
        self.signal_sigma = PL.raw_to_sigma(self.signal_raw).astype(np.float32)
        self.signal_sigma_hilbert = np.abs(hilbert(self.signal_sigma)).astype(np.float32)
        
        self.mask = PL.detect_artefact(self.signal_sigma)
        self.nb_artefact = O.ft_count(self.mask,1)
        
        liste_event , liste_event_long, self.liste_artefact = PL.signal_to_dico_event(self.signal_sigma_hilbert,self.mask)

        self.dico_spindle = PL.class_event(liste_event,self.hypnogram)
        self.dico_spindle_long = PL.class_event(liste_event_long, self.hypnogram)
        self.liste_spindle_N2_N3 = self.dico_spindle["2"] + self.dico_spindle["3"]
        self.dico_hypno = PL.count_stage(self.hypnogram)

        self.spindle_index = 0

        self.figure_artefact = D.figure_artefact(self.signal_sigma,self.mask)
        self.figure_distribution = D.figure_distribution(self.signal_raw,self.dico_spindle,self.hypnogram)
        self.figure_spindle = D.figure_spindle(self.signal_raw,self.signal_sigma,self.dico_spindle,self.spindle_index,self.liste_artefact)
        self.figure_hypnogram = D.figure_hypnogram(self.hypnogram)

        self.msg_spindle = D.msg_spindle(self.dico_spindle,self.dico_hypno)
        self.msg_artefact = D.msg_artefact(self.nb_artefact,self.liste_artefact,len(self.signal_raw))
        self.msg_hypno = D.msg_hypno(self.hypnogram)
        self.msg_global = self.msg_spindle + "\n" + self.msg_artefact 
        
    def next(self,x):
        if self.spindle_index + x < len(self.liste_spindle_N2_N3):
            self.spindle_index += x
            self.figure_spindle = D.figure_spindle(self.signal_raw,self.signal_sigma,self.dico_spindle,self.spindle_index,self.liste_artefact)

    def prev(self,x):
        if self.spindle_index - x > 0:
            self.spindle_index -= x
            self.figure_spindle = D.figure_spindle(self.signal_raw,self.signal_sigma,self.dico_spindle,self.spindle_index,self.liste_artefact)
