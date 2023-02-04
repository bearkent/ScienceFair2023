import sounddevice as sd
import numpy as np
import scipy
from wave import open
import matplotlib.pyplot as plt 
from fix import fix
from datetime import datetime

def record(duration, freq):
    
    print("recording")
    
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, dtype=float)
    sd.wait()
    
    return PowerSpectrum(freq, recording)
    
class Sound:
    
    def __init__(self, freq, numpyarray):
        
        self.freq = freq
        self.numpyarray = numpyarray
        
        self.xs = np.linspace(0, len(numpyarray)/freq, freq)
        self.ys = numpyarray
        
    def plot(self):
        
        plt.plot(self.xs, self.ys)
        
    def play(self):
        
        print("playing audio")
        
        start_time = datetime.now()
        
        sd.play(self.ys, self.freq)
        sd.wait()
        
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))

class FFT(Sound):
    
    def __init__(self, freq, numpyarray):
        
        self.freq = freq
        self.numpyarray = numpyarray
        
        self.xs = np.linspace(0, len(numpyarray)/freq, freq)
        self.ys = numpyarray

        
    def FFT(self):
        
        self.xs = np.fft.rfft(self.xs)
        self.ys = abs(np.fft.rfft(self.ys))
        
        return self.xs, self.ys
        
class PowerSpectrum(FFT):
    
    def __init__(self, freq, numpyarray):
 
        self.freq = freq
        self.numpyarray = numpyarray
        
        self.xs = np.linspace(0, len(numpyarray)/freq, freq)
        self.ys = numpyarray
        
    def powerspecturm(self):
        
        plt.plot(abs(np.fft.rfft(self.ys)))
        
        
# record(1, 44100).powerspecturm()


# prevents the popup plot from deleting itself after creation
fix()