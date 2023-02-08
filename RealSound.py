import sounddevice as sd
import numpy as np
import scipy
from wave import open
import matplotlib.pyplot as plt 
from fix import fix
from datetime import datetime
import pydub

def record(duration: float, samplingfreq: int) -> None:
    
    print("recording")
    
    recording = sd.rec(int(duration * samplingfreq), samplerate=samplingfreq, channels=1, dtype=float)
    sd.wait()
    
    return PowerSpectrum(samplingfreq, recording)
    
def read(samplingfreq: int, file) -> 'Sound':
    
    ifile = open(file)
    samples = ifile.getnframes()
    audio = ifile.readframes(samples)
    
    # Convert buffer to float32 using NumPy                                                                                 
    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
    audio_as_np_float32 = audio_as_np_int16.astype(np.float32)
    
    # Normalise float32 array so that values are between -1.0 and +1.0                                                      
    max_int16 = 2**15
    audio_normalised = audio_as_np_float32 / max_int16
    
    return Sound(samplingfreq, audio_normalised)

def sine(duration: float, frequency: float, samplingfreq: int, amplitude: float) -> 'Sound':
    
    if samplingfreq==None: samplingfreq=duration*frequency*50
    
    xs = np.linspace(0, duration, samplingfreq)
    
    ys = amplitude*np.sin(xs*2*np.pi*frequency)
        
    return Sound(samplingfreq, ys)

class Sound:
    
    def __init__(self, samplingfreq: int, numpyarray: np.array):
        
        self.samplingfreq = samplingfreq
        self.numpyarray = numpyarray
        
        self.xs = np.linspace(0, len(numpyarray)/samplingfreq, samplingfreq)
        self.ys = numpyarray
        
    def __len__(self) -> int:
        return len(self.ys)    
        
    def plot(self) -> None:
        
        plt.plot(self.xs, self.ys)  
        
    def play(self) -> None:
        
        print("playing audio")
        
        start_time = datetime.now()
        
        sd.play(self.ys, self.samplingfreq)
        sd.wait()
        
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))

    def fft(self) -> 'FFT':
        return FFT(self)
    
class FFT:
    
    def __init__(self, sound: Sound):
        
        self.sound = sound
        self.ys = np.fft.rfft(sound.numpyarray)
        self.xs = np.fft.rfft(np.linspace(0, len(sound)/self.sound.samplingfreq, self.sound.samplingfreq))
    
    def __len__(self) -> int:
        return len(self.ys) 
        
    def ifft(self) -> Sound:
        
        self.xs = np.fft.irfft(self.xs)
        self.ys = np.fft.irfft(self.ys)
        
        return Sound(self.samplingfreq, self.ys)
    
    def plot(self) -> None:

        plt.plot(self.xs, self.ys)
        
class PowerSpectrum:
    
    def __init__(self, fft: FFT):
        self.fft = fft    
        self.xs = np.linspace(0, len(fft)/fft.sound.samplingfreq, fft.sound.samplingfreq)
        self.ys = fft.ys
    
    def __len__(self) -> int:
        return len(self.ys) 
    
    def plot(self) -> None:
        
        plt.plot(self.ys) #y values on the graph are a function of the sampling frequency * amplitude / 2
        
    def max(self) -> float:
        
        return np.max(self.ys)
        
        
# read(44100, "audio.wav").play()

# fig = plt.figure()
# sinewave = sine(1, 10, 10, 1)
# sinewave.plot()
# fft = sine(1, 10, 10, 1).fft()
# ifft = fft.ifft()
# ifft.plot()
# fig.show()

fft = sine(100, 10, 100, 1).fft()
powerspecturm = PowerSpectrum(fft)
print(powerspecturm.max())
powerspecturm.plot()

# prevents the popup plot from deleting itself after creation
fix()