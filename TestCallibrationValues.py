import numpy as np
import RealSound as rs
import matplotlib.pyplot as plt
from fix import fix

vals = np.load('CallibrationValues1.npy')
xs = np.array(vals[0])
ys = np.array(vals[1])

plt.plot(xs, ys)
plt.xlabel('Frequency')
plt.ylabel('Spectal Power')
plt.title('First Iteration Test Values')
fix()

vals = np.load('FixedValues1.npy')
xs2 = np.array(vals[0])
ys2 = np.array(vals[1])

plt.plot(xs2, ys2)
plt.xlabel('Frequency')
plt.ylabel('Spectal Power')
plt.title('Second Iteration Test Values')
fix()

plt.show()

# ys = rs.meaninverse(ys)
# f = rs.cubicspline(xs, ys)
# rs.plotspline(f)
# plt.show()
# fix()


