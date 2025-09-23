# SleepSpindleAnalyse
This Script can analyse an EEG record during sleep with a focus on Sleep Spindles. It is adapted to DREEM open datasets. It work with .h5 files with at least the EEG raw signal (µV) and the hypnogram. The channel used can be modified in the script. This scripts are writed in Python langage in 3.12.0 version and needs some packages to work.

==================================================================================================================================================================
Before to run the code you must install some packages with this command in the terminal:

>pip install mne matplotlib numpy h5py scipy

I advice you to use a python virtual environment but it's not necessary to run correctly the code

==================================================================================================================================================================

To download a data file to test the script you can go on : https://github.com/Dreem-Organization/dreem-learning-open?tab=readme-ov-file and select one file and run the script with. This is the DREEM open source data set. One file is corresponding at one night EEG recording of one persone. You can also go on https://drive.google.com/file/d/1E42RW1AsX6By_oXP5eRR6ONXeyKraps-/view?usp=drive_link and download one of the file that I used to test and ajust my scripts.

To run correctly the script you must run the "Interface.py" file after changing the variable "File" in the "Paramètres.py" file with the path of the data file.h5 you just downloaded from DREEM open source data set.

If you want you can just run the "Interface.py" file, write the path of your data file in the entry of the window and click on "Analyse" button, you will see some graphics and informations on sleep spindles and macro structure of sleep

the path should look like : C:\Users\YourName\Desktop\data.h5

==================================================================================================================================================================

How to read and interpret graphics : 

The first graphic "Représentation des artefacts" represent what we considere as an artefact in the signal. All point over 50µV or under -50µV are considered as artefac of the record because in sigma band the signal amplitude usually stay in this interval. So this graphic is just a representation of what will be not interpreted as correct record.  







