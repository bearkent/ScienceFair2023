import RealSound
import numpy as np
import matplotlib.pyplot as plt

def func(x):
    
    x *=2

def multiply(fft, f: np.array):

        i = 0
        
        print('multiplying')
        
        fft.ys = np.real(np.fft.ifft(fft.ys))
        fft.ys = fft.ys.astype(int)
        
        while i < len(fft.ys):
            
            fft.ys[i] *= f(i)
            
            i +=1
            
        return fft.ys
    
sound = RealSound.newread('flamenco.wav')
fft = sound.fft()
print(fft.ys)
fft.ys = multiply(fft, func)
print(fft.ys)
