import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)

import numpy as np
from scipy.stats import norm


result = []

DELTA = 1

MIU = 0

BIGN = 100

xs = np.arange(-2,2,0.05)
ys = np.arange(-2,2,0.05)

# randsx = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=False)
# randsy = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=False)


X, Y = np.meshgrid(xs, ys)
Z = ((Y-X)/2+np.abs(Y-X)/2)/(norm.pdf(X)-norm.cdf(-X)*X)+((X-Y)/2+np.abs(X-Y)/2)/(norm.pdf(Y)-norm.cdf(-Y)*Y)

ax.plot_surface(X,Y,Z,rstride=1, cstride=1, cmap='rainbow')
plt.show()
