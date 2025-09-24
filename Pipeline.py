import h5py
import mne
import numpy as np
from scipy.signal import hilbert
import Parametres as P
import Outils_2 as O


"""
Les données utilisées viennent du DREEM Open Dataset (DOD-H)
"""
################################## 1 ère étape #######################################

# print("Etape 1 Import des données...")

def import_data(file):
    Raw = h5py.File(file, 'r')
    signal = Raw["signals"]["eeg"][P.Channel][:]
    hypnogram = Raw["hypnogram"][:]
    return signal, hypnogram

# signal , hypnogram = import_data(P.File)
# print(signal)

################################## 2 ère étape #######################################

# print("Etape 2 nettoyage des fréquences...")

def clean_data_frequency(raw, fmin, fmax,canal, sf):
    info = mne.create_info(ch_names=[canal], sfreq=sf, ch_types='eeg')
    data = mne.io.RawArray(raw, info)
    data = data.notch_filter(freqs=50, notch_widths=2)
    data = data.filter(fmin, fmax)
    print("=====================================")
    print(f"unité de référence =  {data.info['chs'][0]['unit']}")
    print("=====================================")

    return data

def separate_band(data):
    
    """
    --> permet de découper le signal en fonction des bandes fréquences stoquées dans "Dict_wave".
    
    --> retourne un dictionnaire avec en clées, les noms des bandes fréquences interessantes ("delta, theta, 
    alpha, sigma, beta") et en valeur les fréquences associées sous forme de tuple ("(0.5,4)","(4,8)","...")

    """

    dico_data = {}

    for i in range(len(P.Dict_wave)):
        key = list(P.Dict_wave.keys())[i]
        fmin, fmax = P.Dict_wave[key]
        data_band = data.copy().filter(fmin, fmax)
        dico_data[key] = data_band.get_data()[0]

    return dico_data

def raw_to_sigma(signal):

    # on filtre les frequences inutiles
    signal_clean = clean_data_frequency([signal],P.Fmin,P.Fmax,P.Channel,P.SF)

    # on sépare les bandes fréquence pertinente avec le sommeil
    signal_clean_separate = separate_band(signal_clean)

    # on selectionne uniquement la bande fréquence qui nous interesse pour la detection de sleep spindle
    return signal_clean_separate["sigma"].astype(np.float32)

# sigma_signal = raw_to_sigma(signal)

################################## 3 ère étape #######################################

# print("Etape 3 --> nettoyage des artefacts...")

"""
Nettoyage des artefacts : point > 50 µV
"""

def detect_artefact(signal, treshold = 50):

    """
    Le but est de parcourir le signal et de repérer chaque instant où le signal dépasse 50 µV
    ce qui veut probablement dire que le point mesuré est un artefact. On enregistre ces instants
    dans "mask" que l'on garde pour analyser le signal plus tard
    """

    mask = np.zeros(len(signal), dtype=np.uint8)

    for i,el in enumerate(signal):
        if np.abs(el) > treshold : 
            mask[i] = 1

    return mask 

# mask = detect_artefact(sigma_signal)
# count = O.ft_count(mask,1)
# print(f"nombre d'artefact trouvés : {count}")
# print(f"proportion d'artefact dans le signal = {round((count/len(mask))*100,1)}%")


################################## 4 ère étape #######################################

# print("Etape 4 --> transformée de Hilbert...")

"""
analyse du signal hilbert : le but est de trouver des pic d'activité bref et soudain
"""

# sigma_hilbert_signal = np.abs(hilbert(sigma_signal))


################################## 5 ère étape #######################################

# print("Etape 5 --> parcourir le signal...")

"""
Parcour du signal par fenetre de 30 secondes. calcul de la moyenne et de l'ecart type de la fenêtre 
pour définir un seuil qui determine si il y a un pic d'activité soudain (activité plus forte
qu'habituellement). S'il y aun pic d'activité alors on considère que c'est un Sleep Spindle
"""

def detect_spindle(signal): 
    window = P.Fenetre
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

# print("Etape 6 filtre des faux fuseaux...")

"""
on supprime les faux évènements c'est à dire les pic d'activité trop court (< 0.5 seconde)
et on fusionne deux detection si elles sont trop proche les une des autres
"""
def fusion_fuseaux(liste):
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



def filtre_faux_fuseaux(liste,mask):
    
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
    liste_spindle = fusion_fuseaux(liste_spindle)
    liste_spindle, liste_spindle_long, liste_artefact = filtre_faux_fuseaux(liste_spindle,mask)
    return liste_spindle,liste_spindle_long, liste_artefact

# liste_spindle,liste_spindle_long = signal_to_dico_event(sigma_hilbert_signal,mask)
# O.affiche_liste(liste_spindle)
# O.affiche_liste(liste_spindle_long)




################################## 7 ème étape #######################################

"""
On croise les Spindles détectés avec l'hypnogramme. On sait desormais combien de 
spindle ont été detecté dans chaque stade de sommeil ce qui peut aider à valider
notre modèle car les spindles ne sont présent qu'en N3 et N2 en général (plus en 
N2 qu'en N3)
"""
# pourquoi 7500 ?
# 7500 = 250 x 30 --> 250 point par seconde avec des fenetre de 30 secondes

def classer_event(liste,hypno):
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

# dico_spindle = classer_event(liste_spindle,hypnogram)
# liste_spindle_N2 = dico_spindle["2"]
# liste_spindle_N3 = dico_spindle["3"]
# print(f"nombre de spindle detecté en N3 = {len(liste_spindle_N3)}, en N2 = {len(liste_spindle_N2)}")

#################################### Partie 8 ############################


"""
Bonus, pour avoir des statistiques concernant l'hypnogram ou les spindles
qui peuvent être interessantes
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

# def affiche_dico_hypno(dico):
#     for key,value in dico.items():
#         print(f"{key} --> {round(value/len(hypnogram)*100,1)}% --> {O.sec_to_hms(value * 30)}")

# dico_hypno = count_stage(hypnogram)
# affiche_dico_hypno(dico_hypno)