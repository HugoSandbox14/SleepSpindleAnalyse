
def count_stage(hypno):
    dico = {
        "0" : 0,
        "1" : 0,
        "2" : 0,
        "3" : 0,
        "4" : 0,
        "-1" : 0,
    }

    dico_2 = {
        "2" : 0,
        "3" : 0
    }
    liste = []
    liste_N2_N3 = []
    for el in hypno:
        dico[str(el)] += 0.5
        if str(el) == "2" or str(el) == "3":
            dico_2[str(el)] += 0.5
    for el in dico.values():
        liste.append(el)
    for el in dico_2.values():
        liste_N2_N3.append(el)
    return liste, liste_N2_N3

def ft_count(liste,n):
    count = 0
    for el in liste:
        if el == n:
            count += 1

    return count

def fusion_tuple(tuple1, tuple2):
    return (tuple1[0], tuple2[1])

def is_near(tuple1, tuple2, duration_between):
    if abs(tuple1[1] - tuple2[0]) <= duration_between:
        return True
    else:
        return False
    
def affiche_liste(liste, start = None, end = None):
    print("==========================")
    print("affichage de la liste")
    print("==========================")

    for i, el in enumerate(liste[start:end]):
        print(el, end = " ")
        if i % 20 == 0:
            print()

def sec_to_hms(time):
    h = 0
    m = 0
    s = time
    while s >= 3600:
        h += 1
        s -= 3600
    while s >= 60:
        m += 1
        s -= 60
    return f"{h}h {m}m {s}s"


def mask_to_index(mask):
    liste = []
    for i, el in enumerate(mask):
        if el == 1:
            liste.append(i)
    return liste

def index_to_artefact(liste,signal):
    artefact = []
    for el in liste:
        artefact.append(signal[el])
    return artefact

def dico_to_list(dico):
    keys = dico.keys()
    liste = []
    for key in keys:
        liste += dico[key]
    return liste

def ranger(liste):
    for i in range(len(liste)):
        current = liste[0]
        index = 0
        for j in range(len(liste)-i-1):
            if current[0] < liste[j+1][0]:
                
                index = j+1
                current = liste[j+1]
        liste[index] = liste[-1-i]
        liste[-1-i] = current
    return liste