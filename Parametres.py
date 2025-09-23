File = "C:\\Users\\hugop\\Desktop\\data_1.h5"
Channel = "C3_M2"
SF = 250
Fmin,Fmax = 0.3, 20

Dict_wave = {
    "delta": (0.3, 4),
    "theta": (4, 8),
    "alpha": (8, 12),
    "sigma": (12, 16),
    "beta": (16, 20),
}

Time = 1                                 # taille de la fenêtre glissante en minute
Fenetre = int(250 * 60 * Time)           # fenetre glissante (car frequence d'échantillonage = 250)

