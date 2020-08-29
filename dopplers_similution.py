import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio
from tkinter import *
import pyaudio
from PIL import ImageTk, Image

def genSinAudio(audio_len, frq, fs = 44100):
    f = frq
    sig = [np.sin(2 * np.pi * f * i) for i in np.linspace(0, audio_len, fs * audio_len)]
#     plt.figure(figsize = (20, 10))
#     plt.plot(np.linspace(0, 5, len(sig)), sig)

    #return Audio(data = sig, rate = fs, autoplay = True)
    return np.array(sig, dtype = np.float32)

def realTimeAudio():
    RATE    = 44100
    CHUNK   = 1024
    p = pyaudio.PyAudio()
    player = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True,
    frames_per_buffer=CHUNK)

    player.write(genSinAudio(1, dopplerShift(sliderS.get(), sliderD.get(), sliderF.get())).tostring())

    p.terminate()

def dopplerShift(sourceV, detectV,ogF):
    vs = sourceV # velocity of the source
    vd = detectV # velocity of the detector
    v = 343 # speed of sound m/s
    # -vs -> higher freq, coming toward detector
    # +vs -> lower freq, away
    # -vd -> lower freq, running away from source
    # +vd -> higher freq, coming toward source
    newF = ogF * ((v+vd)/(v+vs))
    return newF

def configNewFText():
    labelNF.config(text = "Frequency: " + str(dopplerShift(sliderS.get(), sliderD.get(), sliderF.get())) + " Hz")

root = Tk()
so = Frame(master = root)
source = Frame(master = root)
detector = Frame(master = root)
global velS
global velD
global sound
global labelNF
velS = IntVar()
velD = IntVar()
sound = IntVar()

# Image
img = ImageTk.PhotoImage(Image.open("lab.jpg").resize((859, 200)))
panel = Label(root, image = img)
panel.pack(fill = BOTH, expand = True)

# Frequency Configurations
labelF = Label(so, text = "Change Frequency of the Source Sound (Hz):")
sliderF = Scale(so, variable = sound, from_ = 100, to = 2000, orient = HORIZONTAL)

# Source Configurations
labelS = Label(source, text = "Change Velocity of Source (m/s):")
dirS = Label(source, text = "{a:<20}{b:>20}".format(a = "Toward Detector", b = "Away from Detector"))
sliderS = Scale(source, variable = velS, from_ = -20, to = 20, orient = HORIZONTAL)

# Detector Configurations
labelD = Label(detector, text = "Change Velocity of Detector (m/s):")
dirD = Label(detector, text = "{a:<20}{b:>20}".format(a = "Away from Source", b = "Toward Source"))
sliderD = Scale(detector, variable = velD, from_ = -20, to = 20, orient = HORIZONTAL)

labelNF = Label(root, text = "Frequency: " + str(dopplerShift(sliderS.get(), sliderD.get(), sliderF.get())) + " Hz")
# Button to Run
button = Button(root, text = "Run", command = lambda:[realTimeAudio(), configNewFText()])

so.pack(fill = BOTH, expand = True)
labelF.pack(fill = BOTH, expand = True)
sliderF.pack(fill = BOTH, expand = True)

source.pack(fill = BOTH, expand = True)
detector.pack(fill = BOTH, expand = True)

labelS.pack(fill = BOTH, expand = True)
dirS.pack(fill = BOTH, expand = True)
sliderS.pack(fill = BOTH, expand = True)

labelD.pack(fill = BOTH, expand = True)
dirD.pack(fill = BOTH, expand = True)
sliderD.pack(fill = BOTH, expand = True)

button.pack(fill = BOTH, expand = True)
labelNF.pack(fill = BOTH, expand = True)

mainloop()
