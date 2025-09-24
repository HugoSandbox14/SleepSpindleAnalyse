# **SleepSpindleAnalyse**

This script can analyze an EEG recording during sleep with a focus on **sleep spindles**.
It is adapted to the **DREEM open datasets** and works with `.h5` files that contain at least the **EEG raw signal (µV)** and the **hypnogram**.
The EEG channel used can be modified directly in the script.

These scripts are written in **Python 3.12.0** and require some external packages to run.

---

### **Installation**

Before running the code, you must install the required packages using the following command in your terminal:

```bash
pip install mne matplotlib numpy h5py scipy
```

I recommend using a **Python virtual environment**, but it is **not mandatory** for the script to work correctly.

---

### **Download Example Data**

To test the script, you can download a data file from the **DREEM open-source dataset**:
[https://github.com/Dreem-Organization/dreem-learning-open](https://github.com/Dreem-Organization/dreem-learning-open)

Each file corresponds to **one full-night EEG recording** of one person.

Alternatively, you can download one of the files I used to test and adjust my scripts on my Google Drive:
[Google Drive link](https://drive.google.com/file/d/1E42RW1AsX6By_oXP5eRR6ONXeyKraps-/view?usp=drive_link)

---

### **How to Run the Script**

1. After downloading a `.h5` data file, **update the variable `File`** in the `Paramètres.py` file with the **path to your data file**.
   Example:

   ```
   C:\Users\YourName\Desktop\data.h5
   ```
2. Run the `Interface.py` file.
3. Alternatively, you can just launch `Interface.py`, **enter the path** to your data file in the window, and click the **"Analyse"** button.
   The program will then display plots and information about **sleep spindles** and the **macrostructure of sleep**.

---

### **Understanding the Graphics**

#### **1. Artefact Representation ("Représentation des artefacts")**

This graph shows what is considered an **artefact** in the signal.
The displayed signal is **filtered in the sigma band** (12–16 Hz).

* All points **above +50 µV** or **below –50 µV** are marked as artefacts because, in the sigma band, the signal amplitude usually stays within this range.
* If a detected spindle contains **too many artefact points (more than 10, arbitrary threshold)**, it will **not be counted** as a real sleep spindle.

---

#### **2. Hypnogram and Spindle Distribution**

The bottom-left plot shows:

* **Classic hypnogram**: the different **sleep stages** over time.
* **Spindle distribution**: each line represents a detected spindle, and its **color corresponds to the stage** where it was detected:

  * **Green** → N2 stage
  * **Yellow** → N3 stage
  * **Orange** → N1 or Wake stage
  * **Red** → REM or Unknown stage

Sleep spindles are **normally found in N2 and N3 stages** (more in N2).
If most detected spindles are green or yellow, the detection results are **consistent** with the expected definition of sleep spindles.

---

#### **3. Spindle Event View ("Événement")**

This plot shows **one detected sleep spindle** in detail:

* The top graph is a **zoomed-in view** of the EEG signal around the spindle (highlighted area).
* Below it, you see the **entire signal**, with:

  * **Red dashed lines** → current spindle location (the one shown above).
  * **Black dashed lines** → spindle candidates **rejected due to artefacts**.

Use the **">>"** (next) and **"<<"** (previous) buttons to navigate through all detected spindles.
The number between the arrows sets how many events to skip when pressing the button.

---

#### **4. Summary Information**

Below the plots, you’ll see:

* **Number of detected spindles** in N2 and N3 stages.
* **Artefact statistics** for the recording.

---

#### **5. Sleep Stage Proportion**

The final graph shows the **distribution of sleep stages** using a bar plot.
Typical proportions are approximately:

* N1 → \~5%
* N2 → \~45%
* N3 → \~25%
* REM → \~25%

---

### **Project Goal**

The main goal of this small project is **to improve my programming skills** by:

* Learning how to **open and read files**,
* Understanding how datasets work,
* Applying **basic statistics**,
* Presenting results with **plots and descriptions**.

This is **only an exercise project**, not a validated sleep spindle detection tool, even though some results **match well with the expected definition** of sleep spindles.

---

**Thank you for reading!**

---



  

