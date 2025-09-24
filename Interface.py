import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import Class as C
from Parametres import File
import affichage as a
import Pipeline as PL
import Outils_2 as O
import matplotlib.pyplot as plt

current_canvas = None

Width, Height = 450, 330  
root = tk.Tk()
root.title("Detection de fuseaux de sommeil")
root.geometry("1200x650")

entry = tk.Entry(root, width = 35)
entry.insert(0,File)
entry.place(x = 540, y = 20)

label = tk.Label(root, text="", width = 70, height = 10, justify = 'left')
label.place(x = 0, y = 100)

def affiche_figure(figure,x,y,width,height):
    canvas = FigureCanvasTkAgg(figure,master = root)
    canvas.draw()
    canvas.get_tk_widget().place(x= x, y = y, width = width, height = height)
    return canvas

def get_stats():
    Analyse = C.Analyse_Object(entry.get())
    affiche_figure(Analyse.figure_artefact,10,100,Width,Height)
    affiche_figure(Analyse.figure_distribution,10,450,Width,Height)
    current_canves = affiche_figure(Analyse.figure_spindle,510,100,Width,Height)
    affiche_figure(Analyse.figure_hypnogram,1020,100,Width,Height)
    a.get_stat(Analyse.dico_spindle,Analyse.dico_hypno)
    text_1 = tk.Label(root, text=Analyse.msg_global, width = 72, height = 10, justify = 'left',font=("Comic", 11))
    text_1.place(x=465,y=450)
    text_2 = tk.Label(root, text=Analyse.msg_hypno, width = 55, height = 10, justify = 'left',font=("Comic", 11))
    text_2.place(x=1020,y=450)

    def suivant(Analyse,x):
        global current_canvas
        Analyse.next(x)
        if current_canvas is not None:
            plt.close(current_canvas.figure)
            current_canvas.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(Analyse.figure_spindle, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=510, y=100, width=Width, height=Height)

        current_canvas = canvas

    def precedent(Analyse,x):
        global current_canvas
        Analyse.prev(x)
        if current_canvas is not None:
            plt.close(current_canvas.figure)
            current_canvas.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(Analyse.figure_spindle, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=510, y=100, width=Width, height=Height)

        current_canvas = canvas

    button_2_1 = tk.Button(root,text = ">1>",command =lambda : suivant(Analyse,1)).place(x = 970, y = 150)
    button_3_1 = tk.Button(root,text = "<1<",command = lambda : precedent(Analyse,1)).place(x =  470, y = 150)
    button_2_10 = tk.Button(root,text = ">10>",command =lambda : suivant(Analyse,10)).place(x = 970, y = 180)
    button_3_10 = tk.Button(root,text = "<10<",command = lambda : precedent(Analyse,10)).place(x =  470, y = 180)
    button_2_25 = tk.Button(root,text = ">25>",command =lambda : suivant(Analyse,25)).place(x = 970, y = 210)
    button_3_25 = tk.Button(root,text = "<25<",command = lambda : precedent(Analyse,25)).place(x =  470, y = 210)

button = tk.Button(root, text="Analyse", command= get_stats)
button.place(x = 760, y = 17)


root.mainloop()
