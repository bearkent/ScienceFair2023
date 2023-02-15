import RealSound
import matplotlib.pyplot as plt

sound = RealSound.newread('flamenco.wav')
sound.play()
plt.plot(sound.ys)


from fix import fix
fix()
