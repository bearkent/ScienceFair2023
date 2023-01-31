from thinkdsp import SquareSignal
from thinkdsp import decorate
from audio2 import play_audio

signal = SquareSignal(1000)
wave = signal.make_wave(duration=10, framerate=16000)
wave.apodize()
wave.write("square.wav")
#play_audio("sound.wav")
play_audio("square.wav")


# duration = signal.period*100
# segment = signal.make_wave(duration, framerate=100000)
# # segment.plot()
# spectrum = segment.make_spectrum()
# spectrum.plot()
# decorate(xlabel='Frequency (s)')

from fix import fix
fix()