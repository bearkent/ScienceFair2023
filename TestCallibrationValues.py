import numpy as np
import RealSound as rs
from fix import fix

vals = np.load('CallibrationValues1.npy')
xs = np.array(vals[0])
ys = np.array(vals[1])

ys = abs(ys/len(xs))**2

# ys = rs.meaninverse(ys)
f = rs.cubicspline(xs, ys)
rs.plotspline(f)
fix()
