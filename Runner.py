import numpy as np
import RealSound as rs
from fix import fix
import matplotlib.pyplot as plt

vals = np.load('CallibrationValues1.npy')
xs = np.array(vals[0])
ys = np.array(vals[1])
ys = rs.meaninverse(ys)
print(f"DEBUG: {max(xs)}")
f = rs.cubicspline(xs, ys)
# plt.figure()
# rs.plotspline(f)
# plt.show()
# fix()

sound = rs.soundread('guitarrecording.wav')
# sound.plot()

fix()
# sound.play()
fft = sound.fft()

powerspectrum = rs.PowerSpectrum(fft)
# plt.figure()
# powerspectrum.plot()
# fix()

f2 = lambda x: 0.0 if x > 20000 else f(x)

newfft = fft.multiply(f2)

newpowerspectrum = rs.PowerSpectrum(newfft)
# newpowerspectrum.plot()
# plt.xlabel('Frequency')
# plt.ylabel('Spectral Power')
# plt.title('Adjusted Power Spectrum of Guitar')
# fix()

newsound = newfft.ifft()

newsound.plot()
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Adjusted Guitar Recording')
fix()

newsound.play()



# rs.plotspline(f)
# plt.xlabel('Frequencies')
# plt.ylabel('Spectral Power')
