from typing import Callable
import sounddevice as sd
import soundfile as sf
import numpy as np
# import pickle
# from wave import open
import matplotlib.pyplot as plt 
from datetime import datetime
import asyncio
from scipy.interpolate import CubicSpline
# from fix import fix
from scipy.io.wavfile import read, write
# from os.path import dirname, join as pjoin
# from scipy.io.wavfile import write

#TODO: document all code before the fair

def record(duration: float, samplingfreq: int) -> 'Sound':
    print("recording")
    #TODO: record to float or int???
    recording = sd.rec(int(duration * samplingfreq), samplerate=samplingfreq, channels=1, dtype=float)
    sd.wait()
    return Sound(samplingfreq, recording)

def soundread(file) -> 'Sound':
    samplingfreq, ys = read(file)
    return Sound(samplingfreq, ys)


def sine(duration: float, frequency: float, samplingfreq: int, amplitude: float) -> 'Sound':
    n = int(duration*samplingfreq)
    xs = np.arange(0, n+1) / samplingfreq
    ys = amplitude*np.sin(xs*2*np.pi*frequency)
    return Sound(samplingfreq, ys)


class Sound:
    
    def __init__(self, samplingfreq: int, ys: np.array):
        self.samplingfreq = samplingfreq
        self.ys = ys
        self.xs = np.arange(0, len(ys)) / samplingfreq

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
        ys = np.fft.rfft(self.ys, axis=0)
        return FFT(self.samplingfreq, ys)


class FFT:

    def __init__(self, samplingfreq: int, ys: np.array):
        self.samplingfreq = samplingfreq
        self.ys = ys
        samples = len(ys)
        self.xs = np.linspace(0, samples/2, int(samples/2)+1) * (samplingfreq/samples)
    
    def __len__(self) -> int:
        return len(self.ys) 
        
    def ifft(self) -> Sound:
        ys = np.fft.irfft(self.ys, axis=0)
        #TODO: what should the types be for sounds?! int or float?

        
        return Sound(self.samplingfreq, ys)
    
    def plot(self) -> None:
        plt.plot(self.xs, self.ys)

    def multiply(self, f: Callable[[float],float]) -> 'FFT':
        newys = np.copy(self.ys)

        print('multiplying')

        #TODO: vectorize
        for i in range(0, int(len(self.ys)/2)):
            
            newys[i] = self.ys[i]*f(self.xs[i])  
            
        return FFT(self.samplingfreq, newys)
    

class PowerSpectrum:
    
    def __init__(self, fft: FFT):
        self.xs = fft.xs
        self.ys = abs(fft.ys)^2
    
    def __len__(self) -> int:
        return len(self.ys) 
    
    def plot(self) -> None:
        plt.plot(self.xs, self.ys)

    #TODO: what should this be doing?
    def max(self) -> float:
        return np.max(self.ys)


#TODO: better name?
async def recordamps(testfreq, step, endfreq, samplingfreq, samplingtime):
    
    amps = []
    freqs = []

    while testfreq <= endfreq:
        
        sinewave = sine(samplingtime, testfreq, samplingfreq, 1)
        
        returnvals = await asyncio.gather(
            asyncio.to_thread(Sound.play, sinewave),
            asyncio.to_thread(record, samplingtime, samplingfreq)
        )
        
        fft = returnvals[1].fft()
        powerspecturm = PowerSpectrum(fft)

        amp = powerspecturm.max()
        amps.append(amp)
        
        freqs.append(testfreq)
        
        testfreq += step
        
    amps = np.array(amps)
    freqs = np.array(freqs)
    vals = [freqs, amps]

    #TODO: save is better as a different function that takes in a filename, so that you can easily run and save multiple tests
    np.save('TestValues1.npy', vals)
    
    return freqs, amps


def meaninverse(ys):
    #TODO: I think there is an avg func
    sums = sum(ys)
    lengths = len(ys)
    mean = sums/lengths
    #makes sure the amps are averaged to 1
    
    ys = mean/ys
    
    return ys


def cubicspline(x, y):
    return CubicSpline(x, y, bc_type='natural')

def plotspline(f):
    
    x_new = np.linspace(1, 20001, 100000)
    y_new = f(x_new)
    
    plt.plot(x_new, y_new)
