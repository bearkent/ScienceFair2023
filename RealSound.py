import sounddevice as sd
import numpy as np
import pickle
from wave import open
import matplotlib.pyplot as plt 
from datetime import datetime
import asyncio
from scipy.interpolate import CubicSpline
from fix import fix
from scipy.io.wavfile import read
from os.path import dirname, join as pjoin
from scipy.io.wavfile import write

def record(duration: float, samplingfreq: int) -> 'Sound':
    
    print("recording")
    
    recording = sd.rec(int(duration * samplingfreq), samplerate=samplingfreq, channels=1, dtype=float)
    sd.wait()
    
    return Sound(samplingfreq, recording)

def read(file):
    
    samplingfreq, ys = read(file)
    return Sound(samplingfreq, ys)
    

def sine(duration: float, frequency: float, samplingfreq: int, amplitude: float) -> 'Sound':

    xs = np.linspace(0, duration, duration*samplingfreq)
    
    ys = amplitude*np.sin(xs*2*np.pi*frequency)
        
    return Sound(samplingfreq, ys)

class Sound:
    
    def __init__(self, samplingfreq: int, numpyarray: np.array):
        
        self.samplingfreq = samplingfreq
        self.numpyarray = numpyarray
        
        self.xs = np.linspace(0, len(numpyarray)/samplingfreq, len(numpyarray))
        self.ys = numpyarray
        
    def __len__(self) -> int:
        return len(self.ys)    
        
    def plot(self) -> None:
        
        plt.plot(self.xs, self.ys)  
        
    def play(self) -> None:
        
        print("playing audio\n")
        
        start_time = datetime.now()
        
        sd.play(self.ys, self.samplingfreq)
        sd.wait()
        
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))
        
    def write(self, file) -> None:
        
        write(file, self.samplingfreq, self.ys)

    def fft(self) -> 'FFT':
        return FFT(self.xs, self.ys, self.samplingfreq, False)
                
    
class FFT:
    
    def __init__(self, xs, ys, samplingfreq, bypass):

        self.samplingfreq = samplingfreq
        
        self.samples = len(ys)
        
        if bypass == False:
            
            self.ys = np.fft.rfft(ys, axis=0)
            
        else:
            
            self.ys = ys
        
        self.xs = xs
        self.xs = np.linspace(0, self.samples/2, int(self.samples/2)+1) * (self.samplingfreq/self.samples)
    
    def __len__(self) -> int:
        return len(self.ys) 
        
    def ifft(self) -> Sound:
        
        self.ys = np.fft.irfft(self.ys, axis=0)
        # self.ys = self.ys.astype(int)
        
        return Sound(self.samplingfreq, self.ys)
    
    def plot(self) -> None:

        plt.plot(self.xs, self.ys)
        fix()
        
    def multiply(self, f: np.array) -> 'FFT':

        newys = np.copy(self.ys)
        
        
        print('multiplying')
        
        for i in range(0, int(len(self.ys)/2)):
            
            if self.xs[i] > 20000:
                
                newys[i] = self.ys[i]*f(self.xs[i])  
            
        return FFT(self.xs, newys, self.samplingfreq, True)
    

class PowerSpectrum:
    
    def __init__(self, fft: FFT):
        self.fft = fft    
        self.xs = fft.xs
        self.ys = abs(fft.ys)^2
    
    def __len__(self) -> int:
        return len(self.ys) 
    
    def plot(self) -> None:
        
        plt.plot(self.xs, self.ys) #y values on the graph are a function of the sampling frequency * amplitude / 2
        fix()
        
    def max(self) -> float:
        
        return np.max(self.ys)

async def recordamps(startfreq, step, endfreq, samplingfreq):
    
    amps = []
    freqs = []
    
    while startfreq <= endfreq:
        
        sinewave = sine(1, startfreq, samplingfreq, 1)
        
        returnvals = await asyncio.gather(
            asyncio.to_thread(Sound.play, sinewave),
            asyncio.to_thread(record, 1, samplingfreq)
        )
        
        fft = FFT(returnvals[1])
        powerspecturm = PowerSpectrum(fft)
        # power spectrum is sq of amplitude??
        amp = powerspecturm.max()
        amps.append(amp)
        
        freqs.append(startfreq)
        
        startfreq += step
        
    amps = np.array(amps)
    freqs = np.array(freqs)
    vals = [freqs, amps]
    np.save('TestValues1.npy', vals)
    
    return freqs, amps

def meaninverse(ys):
    
    sums = sum(ys)
    lengths = len(ys)
    mean = sums/lengths
    #makes sure the values are averaged to 1
    
    ys = mean/ys
    
    return ys

def cubicspline(x, y):
    
    return CubicSpline(x, y, bc_type='natural')

def plotspline(f):
    
    x_new = np.linspace(1, 20001, 100000)
    y_new = f(x_new)
    
    plt.plot(x_new, y_new)
    fix()
