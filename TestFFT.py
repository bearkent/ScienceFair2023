import RealSound
import numpy as np
import matplotlib.pyplot as plt

# array = np.array([1,1,2])
# print(array)
# testfft = np.fft.fft(array)
# print(testfft)
# testifft = np.fft.ifft(testfft)
# print(testifft)

sound = RealSound.newread('flamenco.wav')
sound.play()
plt.plot(sound.ys)
print("{},{}".format(sound.xs, sound.ys))
fft = sound.fft()
# print(fft.ys)
ifft = fft.ifft()
plt.plot(ifft.ys)
print("{},{}".format(ifft.xs, ifft.ys))
ifft.play()
plt.legend()
plt.show()


from fix import fix
fix()