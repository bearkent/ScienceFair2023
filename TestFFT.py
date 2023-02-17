import RealSound
import numpy as np
import matplotlib.pyplot as plt

# array = np.array([1,1,2])
# print(array)
# testfft = np.fft.fft(array)
# print(testfft)
# testifft = np.fft.ifft(testfft)
# print(testifft)

sound = RealSound.sine(1, 10000, 22050, 10)

fft = sound.fft()
plt.plot(fft.ys)
powerspectum = RealSound.PowerSpectrum(fft)
amp = powerspectum.max()
print(amp)

sound2 = RealSound.sine(1, 10000, 88200, 10)
fft2 = sound2.fft()
plt.plot(fft2.ys)
powerspectum2 = RealSound.PowerSpectrum(fft2)
amp2 = powerspectum2.max()
print(amp2)
print("amp/amp2 = {}".format(amp/amp2))


plt.show()


from fix import fix
fix()