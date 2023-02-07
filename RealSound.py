import sounddevice as sd
import numpy as np
import scipy
from wave import open
import matplotlib.pyplot as plt 
from fix import fix
from datetime import datetime
import pydub

def record(duration, freq):
    
    print("recording")
    
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, dtype=float)
    sd.wait()
    
    return PowerSpectrum(freq, recording)
    
def read(freq, file):
    
    ifile = open(file)
    samples = ifile.getnframes()
    audio = ifile.readframes(samples)
    
    # Convert buffer to float32 using NumPy                                                                                 
    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
    audio_as_np_float32 = audio_as_np_int16.astype(np.float32)
    
    # Normalise float32 array so that values are between -1.0 and +1.0                                                      
    max_int16 = 2**15
    audio_normalised = audio_as_np_float32 / max_int16
    
    return Sound(freq, audio_normalised)

def sine(duration, frequency, samplingfreq, amplitude):
    
    if samplingfreq==None: samplingfreq=duration*frequency*50
    
    xs = np.linspace(0, duration, samplingfreq)
    
    ys = amplitude*np.sin(xs*2*np.pi*frequency)
        
    return Sound(samplingfreq, ys)
    
    

    
    

class Sound:
    
    def __init__(self, samplingfreq, numpyarray):
        
        self.freq = samplingfreq
        self.numpyarray = numpyarray
        
        self.xs = np.linspace(0, len(numpyarray)/samplingfreq, samplingfreq)
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

# read(44100, "audio.wav").play()

sine(1, 1, 50, 1).plot()


# prevents the popup plot from deleting itself after creation
fix()