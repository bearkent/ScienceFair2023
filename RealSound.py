import sounddevice as sd
import numpy as np
import scipy
from wave import open
import matplotlib.pyplot as plt 
from fix import fix

fix()

def record(duration, freq):
    
    print("recording")
    
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, dtype=float)
    sd.wait()
    
    return Sound(freq, recording)
    
class Sound:
    
    def __init__(self, freq, numpyarray):
        
        self.freq = freq
        self.numpyarray = numpyarray
        
        self.xs = np.linspace(0, len(numpyarray)/freq, freq)
        self.ys = numpyarray
        
    def plot(self):
        
        plt.plot(self.xs, self.ys)
        
        
    
record(1, 44100).plot()

fix()