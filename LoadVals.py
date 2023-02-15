import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

vals = np.load('TestValues1.npy')
# print(vals)
# plt.plot(vals[0], vals[1])

def cubicspline(x, y):
    
    f = CubicSpline(x, y, bc_type='natural')
    
    return f
    
def plotspline(f):
    
    x_new = np.linspace(1, 20001, 100000)
    y_new = f(x_new)
    
    plt.plot(x_new, y_new)
    
def multiply(fft, f):
    
    xs = fft.xs
    ys = fft.ys
    
    for freq in xs:
        ys[xs.index(freq)] *= f(xs.index(freq))
        
    return ys            
    
plotspline(cubicspline(vals[0], vals[1]))

from fix import fix
fix()