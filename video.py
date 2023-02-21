import numpy as np
import RealSound as rs
import matplotlib.pyplot as plt
from fix import fix

vals = np.load('CallibrationValues1.npy')
xs = np.array(vals[0])
ys = np.array(vals[1])
ys = rs.meaninverse(ys)
f = rs.cubicspline(xs, ys)
f2 = lambda x: 0.0 if x > 20000 else f(x)

sound = rs.soundread('guitarrecording.wav')
sound.play()

fft = sound.fft()
powerspectrum = rs.PowerSpectrum(fft)
powerspectrum.plot()
plt.show()
fix()

newfft = fft.multiply(f2)
newpowerspectrum = rs.PowerSpectrum(newfft)
newpowerspectrum.plot()
plt.show()
fix()

newsound = newfft.ifft()
newsound.play()