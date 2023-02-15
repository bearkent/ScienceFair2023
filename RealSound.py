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
import scipy

def record(duration: float, samplingfreq: int) -> None:
    
    print("recording")
    
    recording = sd.rec(int(duration * samplingfreq), samplerate=samplingfreq, channels=1, dtype=float)
    sd.wait()
    
    return Sound(samplingfreq, recording)
    
def oldread(samplingfreq: int, file) -> 'Sound':
    
    ifile = open(file)
    samples = ifile.getnframes()
    audio = ifile.readframes(samples)
    
    # Convert buffer to float32 using NumPy                                                                                 
    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
    audio_as_np_float32 = audio_as_np_int16.astype(np.float32)
    
    # Normalise float32 array so that values are between -1.0 and +1.0                                                      
    max_int16 = 2**15-1
    audio_normalised = audio_as_np_float32 / max_int16
    
    return Sound(samplingfreq, audio_normalised)

def newread(file):
    
    # data_dir = pjoin(dirname(scipy.io.__file__), 'tests', 'data')
    # wav_fname = pjoin(data_dir, '{}'.format(file))
    
    samplingfreq, ys = read(file)
    
    return Sound(samplingfreq, ys)
    

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
        
        print("playing audio\n")
        
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
        self.ys = abs(np.fft.rfft(sound.numpyarray))
        self.xs = np.fft.rfft(np.linspace(0, len(sound)/self.sound.samplingfreq, self.sound.samplingfreq))
    
    def __len__(self) -> int:
        return len(self.ys) 
        
    def ifft(self) -> Sound:
        
        self.xs = np.fft.irfft(self.xs)
        self.ys = np.fft.irfft(self.ys)
        
        return Sound(self.sound.samplingfreq, self.ys)
    
    def plot(self) -> None:

        plt.plot(self.xs, self.ys)
        
    def multiply(self, f: np.array) -> 'FFT':
        rst = FFT(self.sound)
        
        i = 0
        
        while i < len(rst.ys):
            
            rst.ys[i] *= f(i)
            
            i +=1
            
        return rst
    
    # def multiply1(self, f):
    
    #     xs = fft.xs
    #     ys = fft.ys
    
    #     for freq in xs:
    #         ys[xs.index(freq)] *= f(xs.index(freq))
        
    #     return ys
        
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
    # multiplier = 1/mean #makes sure the values are averaged to 1
    
    ys = mean/ys
    
    return ys

def cubicspline(x, y):
    
    f = CubicSpline(x, y, bc_type='natural')
    
    return f

def plotspline(f):
    
    x_new = np.linspace(1, 20001, 100000)
    y_new = f(x_new)
    
    plt.plot(x_new, y_new)
    fix()

    
# def multiply(fft: FFT, f):
    
#     xs = fft.xs
#     ys = fft.ys
    
#     for freq in xs:
#         ys[xs.index(freq)] *= f(xs.index(freq))
        
#     return ys

# asyncio.run(recordamps(1, 2000, 20001, 44100))

# vals = np.load('TestValues1.npy')
# xs = np.array(vals[0])
# ys = np.array(vals[1])
# ys = meaninverse(ys)
# f = cubicspline(xs, ys)
# # plotspline(f)
# sound = read(44100, 'audio.wav')
# # sound.play()
# # plt.plot(sound.ys)
# fft = FFT(sound)
# print('multiplying')
# fft = fft.multiply(f)
# newsound = fft.ifft()
# newsound.play()
# plt.plot(newsound.ys)
# plt.show()
# fix()


        
# read(44100, "audio.wav").play()

# fig = plt.figure()
# sinewave = sine(1, 10, 10, 1)
# sinewave.plot()
# fft = sine(1, 10, 10, 1).fft()
# ifft = fft.ifft()
# ifft.plot()
# fig.show()

# sine(10, 100, 44100, 10).play()
# fft = record(1, 44100).fft()
# powerspecturm = PowerSpectrum(fft)
# print(powerspecturm.max())
# powerspecturm.plot()

# prevents the popup plot from deleting itself after creation
