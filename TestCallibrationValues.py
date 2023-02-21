import numpy as np
import RealSound as rs
import matplotlib.pyplot as plt
from fix import fix

vals = np.load('CallibrationValues1.npy')
xs = np.array(vals[0])
ys = np.array(vals[1])

plt.plot(xs, ys)
plt.show()
fix()

ys = rs.meaninverse(ys)
f = rs.cubicspline(xs, ys)
rs.plotspline(f)
plt.show()
fix()


