# editable
File = "your/data/file/path/data.h5"
Channel = "C3_M2"
Time = 1                                # time of the window (minute) for detecting spindle 

# not editable
SF = 250
Fmin,Fmax = 0.3, 20
Dict_wave = {
    "delta": (0.3, 4),
    "theta": (4, 8),
    "alpha": (8, 12),
    "sigma": (12, 16),
    "beta": (16, 20),
}

Window = int(250 * 60 * Time)           
