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
import RealSound






vals = np.load('TestValues1.npy')
xs = np.array(vals[0])
ys = np.array(vals[1])
ys = RealSound.meaninverse(ys)
f = RealSound.cubicspline(xs, ys)

sound = RealSound.record(5, 44100)
print(sound.numpyarray)
# plt.plot(sound.ys)
fft = sound.fft()
# plt.plot(fft.ys)
fft = fft.multiply(f)
newsound = fft.ifft()


newsound.play()
newfft = newsound.fft()
plt.plot(newfft.ys)
plt.show()

fix()
# prevents the popup plot from deleting itself after creation