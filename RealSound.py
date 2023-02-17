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
    #TODO: record to float or int???
    recording = sd.rec(int(duration * samplingfreq), samplerate=samplingfreq, channels=1, dtype=float)
    sd.wait()
    return Sound(samplingfreq, recording)
    
# def oldread(samplingfreq: int, file) -> 'Sound':
#     ifile = open(file)
#     samples = ifile.getnframes()
#     audio = ifile.readframes(samples)
#
#     # Convert buffer to float32 using NumPy
#     audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
#     audio_as_np_float32 = audio_as_np_int16.astype(np.float32)
#
#     # Normalise float32 array so that values are between -1.0 and +1.0
#     max_int16 = 2**15-1
#     audio_normalised = audio_as_np_float32 / max_int16
#
#     return Sound(samplingfreq, audio_normalised)

def newread(file):
    samplingfreq, ys = read(file)
    return Sound(samplingfreq, ys)
    

def sine(duration: float, frequency: float, samplingfreq: int, amplitude: float) -> 'Sound':

    #TODO: is this block used?
    if samplingfreq==None: 
        samplingfreq=duration*frequency*50
    
    xs = np.linspace(0, duration, duration*samplingfreq)
    
    ys = amplitude*np.sin(xs*2*np.pi*frequency)
        
    return Sound(samplingfreq, ys)

class Sound:
    
    def __init__(self, samplingfreq: int, numpyarray: np.array):
        
        self.samplingfreq = samplingfreq
        self.numpyarray = numpyarray

        #TODO: is there a better option than linspace or arange -> arange(0,n)* step
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

    def fft(self) -> 'FFT':
        #TODO: fix fft constructor
        return FFT(self.xs, self.ys, self.samplingfreq, False)

class FFT:

    #TODO: constructor looks suspect
    def __init__(self, xs, ys, samplingfreq, bypass):

        self.samplingfreq = samplingfreq
        
        self.samples = len(ys)
        
        if bypass == False:
            
            self.ys = np.fft.rfft(ys, axis=0)
            
        else:
            
            self.ys = ys
        
        
        
        # self.xs = xs
        self.xs = np.linspace(0, self.samples/2, int(self.samples/2)+1) * (self.samplingfreq/self.samples)
    
    def __len__(self) -> int:
        return len(self.ys) 
        
    def ifft(self) -> Sound:
        
        # self.xs = np.linspace(0, len(self.ys)/self.samplingfreq, len(self.ys))
        
        self.ys = np.fft.irfft(self.ys, axis=0)
        # self.ys = self.ys.astype(int)
        
        return Sound(self.samplingfreq, self.ys)
    
    def plot(self) -> None:
        plt.plot(self.xs, self.ys)
        
    def multiply(self, f: np.array) -> 'FFT':
        newys = np.copy(self.ys)

        print('multiplying')

        #TODO: vectorize
        for i in range(0, int(len(self.ys)/2)):
            
            if self.xs[i] > 20000:
                
                newys[i] = self.ys[i]*f(self.xs[i])
            #TODO: looks like a bug
            i +=1    
            
        return FFT(self.xs, newys, self.samplingfreq, True)
    

class PowerSpectrum:
    
    def __init__(self, fft: FFT):
        # self.fft = fft
        self.xs = fft.xs
        self.ys = fft.ys  #TODO: not a power spectrum...
    
    def __len__(self) -> int:
        return len(self.ys) 
    
    def plot(self) -> None:
        #TODO: plot does not include frequency so couldn't verify the power spectrum or fft
        plt.plot(self.ys) #y values on the graph are a function of the sampling frequency * amplitude / 2

    #TODO: what should this be doing?
    def max(self) -> float:
        return np.max(self.ys)

async def recordamps(startfreq, step, endfreq, samplingfreq):
    
    amps = []
    freqs = []

    #TODO: best not to reuse startfreq, since the meaning will be different from the name
    while startfreq <= endfreq:
        
        sinewave = sine(1, startfreq, samplingfreq, 1)
        
        returnvals = await asyncio.gather(
            asyncio.to_thread(Sound.play, sinewave),
            #TODO: should make the sample time configurable
            asyncio.to_thread(record, 1, samplingfreq)
        )
        
        fft = FFT(returnvals[1])
        powerspecturm = PowerSpectrum(fft)

        #TODO: power spectrum is sq of amplitude??
        amp = powerspecturm.max()
        amps.append(amp)
        
        freqs.append(startfreq)
        
        startfreq += step
        
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
    #makes sure the values are averaged to 1
    
    ys = mean/ys
    
    return ys

def cubicspline(x, y):
    return CubicSpline(x, y, bc_type='natural')



def plotspline(f):
    
    x_new = np.linspace(1, 20001, 100000)
    y_new = f(x_new)
    
    plt.plot(x_new, y_new)
