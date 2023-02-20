import RealSound as rs
import matplotlib.pyplot as plt
import numpy as np

vals = np.load("CallibrationValues1.npy")
freqs = vals[0]
amps = vals[1]
amps = rs.meaninverse(amps)
cubicspline = rs.cubicspline(freqs, amps)


sinewave1 = rs.sine(1, 10000, 44100, 10)
sinewave2 = rs.sine(1, 15000, 44100, 3)

sinewave1.ys += sinewave2.ys

fft = sinewave1.fft()
fft = fft.multiply(cubicspline)

powerspectrum = rs.PowerSpectrum(fft)


# powerspectrum.plot()

from fix import fix
fix()