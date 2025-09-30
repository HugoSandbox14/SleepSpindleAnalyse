import h5py
import mne
import numpy as np
from scipy.signal import hilbert
import Settings as S
import Tools as O


"""
Data used come from DREEM Open Dataset (DOD-H)
"""
################################## 1 ère étape #######################################

# print("Step 1 Data import")

def import_data(file):
    Raw = h5py.File(file, 'r')
    signal = Raw["signals"]["eeg"][S.Channel][:]
    hypnogram = Raw["hypnogram"][:]
    return signal, hypnogram

# signal , hypnogram = import_data(S.File)
# print(signal)

################################## 2 ère étape #######################################

# print("Step 2 Clean frequency...")

def clean_data_frequency(raw, fmin, fmax,canal, sf):
    info = mne.create_info(ch_names=[canal], sfreq=sf, ch_types='eeg')
    data = mne.io.RawArray(raw, info)
    data = data.notch_filter(freqs=50, notch_widths=2)
    data = data.filter(fmin, fmax)
    print("=====================================")
    print(f"reference unit =  {data.info['chs'][0]['unit']}")
    print("=====================================")

    return data

def separate_band(data):
    
    """
    --> Allows you to slice the signal according to the frequency bands stored in "Dict_wave".

    --> Returns a dictionary with the names of the frequency bands of interest as keys ("delta, theta,
    alpha, sigma, beta") and the associated frequencies as values in tuple form ("(0.5,4)","(4,8)","...")

    """

    dico_data = {}

    for i in range(len(S.Dict_wave)):
        key = list(S.Dict_wave.keys())[i]
        fmin, fmax = S.Dict_wave[key]
        data_band = data.copy().filter(fmin, fmax)
        dico_data[key] = data_band.get_data()[0]

    return dico_data

def raw_to_sigma(signal):

    # we filter uselesses frequencys
    signal_clean = clean_data_frequency([signal],S.Fmin,S.Fmax,S.Channel,S.SF)

    # We separate the frequency bands relevant to sleep.
    signal_clean_separate = separate_band(signal_clean)

    # We select only the frequency band relevent for sleep spindle detection.
    return signal_clean_separate["sigma"].astype(np.float32)

# sigma_signal = raw_to_sigma(signal)

################################## 3 ère étape #######################################

# print("Step 3 --> cleanning artefacts...")

"""
cleanning artefacts : point > 50 µV
"""

def detect_artefact(signal, treshold = 50):

    """
    The goal is to scan the signal and identify each moment where the signal exceeds 50 µV, 
    which probably means that the measured point is an artifact. We record these moments in 
    "mask" which we keep to analyze the signal later.
    """

    mask = np.zeros(len(signal), dtype=np.uint8)

    for i,el in enumerate(signal):
        if np.abs(el) > treshold : 
            mask[i] = 1

    return mask 

# mask = detect_artefact(sigma_signal)
# count = T.ft_count(mask,1)

################################## 4 ère étape #######################################

# print("Step 4 --> Hilbert transform...")

"""
Hilbert signal analyse : the goal is to find brief and sudden peaks of activity
"""

# sigma_hilbert_signal = np.abs(hilbert(sigma_signal))


################################## 5 ère étape #######################################

# print("Step 5 --> run trough the signal...")

"""
Signal path through 30-second windows. Calculation of the average and standard deviation of 
the window to define a threshold that determines if there is a sudden peak of activity 
(stronger activity than usual). If there is a peak of activity then it is considered a Sleep Spindle
"""

def detect_spindle(signal): 
    window = S.Fenetre
    run = True
    x = 0
    liste_spindle = []
    
    while run:
        if x + window <= len(signal):
            piece = signal[x:x+window]
        else : 
            piece = signal[x:]
            run = False

        median = np.median(piece)
        mad = np.median(np.abs(piece - median))
        sigma = 1.4826 * mad
        treshold_1  = median + 3.5 * sigma
        treshold_2 = median + 2 * sigma

        sous_liste_spindle = detect_spindle_bis(piece,treshold_1,treshold_2,x)
        liste_spindle.extend(sous_liste_spindle)
        x += window
    return liste_spindle

def detect_spindle_bis(piece,tresh_1,tresh_2,start):
    liste = []
    A = True
    for i in range(len(piece)):
        if A == True and piece[i] >= tresh_1 :
            A = False
            debut = start + i
            
        elif A == False and piece[i] < tresh_2 : 
            A = True
            fin = start + i
            liste.append((debut,fin))
    if A == False:  
        liste.append((debut, start + len(piece) - 1))
    return liste

################################## 6 ème étape #######################################

# print("Step 6 filter of false spindle...")

"""
We remove false events, i.e., activity peaks that are too short (< 0.5 seconds)
and we merge two detections if they are too close to each other
"""
def merge_fuseaux(liste):
    i = 0
    res = []
    while(i < len(liste)):
        if i == 0:
            current = liste[0]
        if i+1 == len(liste):
            res.append(current)
            return res
        if O.is_near(current,liste[i+1],100):  
            current = O.fusion_tuple(current,liste[i+1])
        else :
            res.append(current)
            current = liste[i+1]
        i+=1
    return res



def filter_false_spindle(liste,mask):
    
    def delete_artefact(liste,mask):
        liste_clean = []
        liste_artefact = []
        for x,y in liste:
            count = O.ft_count(mask[x:y],1)
            if count > 10:
                # print(f"spindle supprimé (artefact) {O.sec_to_hms(x//250)} à {O.sec_to_hms(y//250)}")
                liste_artefact.append((x,y))
            else :
                liste_clean.append((x,y))
        return liste_clean,liste_artefact
    
    liste_clean, liste_artefact = delete_artefact(liste,mask)

    liste_event = []
    liste_event_long = []
    for x,y in liste_clean:
        if y-x > 550:               # 500 = 2 secondes
            liste_event_long.append((x,y))
        elif y - x >= 125:          # 125 = 0.5 secondes
            liste_event.append((x,y))
    return liste_event, liste_event_long, liste_artefact


# fusion de la detection des spindles et du nettoyage des faux spindles
def signal_to_dico_event(sigma_hilbert_signal,mask):
    liste_spindle = detect_spindle(sigma_hilbert_signal)
    liste_spindle = merge_fuseaux(liste_spindle)
    liste_spindle, liste_spindle_long, liste_artefact = filter_false_spindle(liste_spindle,mask)
    return liste_spindle,liste_spindle_long, liste_artefact

# liste_spindle,liste_spindle_long = signal_to_dico_event(sigma_hilbert_signal,mask)

################################## 7 ème étape #######################################

"""
We cross-reference the detected spindles with the hypnogram. We now know how many 
spindles were detected in each sleep stage, which can help to validate our model because 
spindles are generally only present in N3 and N2 (more in N2 than in N3).
"""
# pourquoi 7500 ?
# 7500 = 250 x 30 --> 250 point par seconde avec des fenetre de 30 secondes

def class_event(liste,hypno):
    dico = {
        "0" : [],
        "1" : [],
        "2" : [],
        "3" : [],
        "4" : [],
        "-1" : [],
    }

    for start, end in liste :
        index = start // 7500
        stade = str(hypno[index])
        dico[stade].append((start,end))
    return dico

# dico_spindle = class_event(liste_spindle,hypnogram)
# liste_spindle_N2 = dico_spindle["2"]
# liste_spindle_N3 = dico_spindle["3"]

#################################### Partie 8 ############################


"""
Bonus: to get statistics about the hypnogram or spindles
which can be interesting
"""

def count_stage(hypno):
    dico = {
        "0" : 0,
        "1" : 0,
        "2" : 0,
        "3" : 0,
        "4" : 0,
        "-1" : 0,
    }
    for el in hypno:
        dico[str(el)] += 30

    return dico