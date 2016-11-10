import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from scipy.stats import norm


result = []

DELTA = 1

MIU = 0

BIGN = 100

xs = np.arange(-2, 2, 0.01)

# randsx = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=False)
# randsy = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=False)


zs1 = [1/(norm.pdf(x)- norm.cdf(-x)* x) for x in xs]
zs2 = [2/((2-x)) for x in xs]
zs3 = [(norm.pdf(x)- norm.cdf(-x)* x) for x in xs]
zs4 = [(2-x)/2 for x in xs]



# plt.plot(xs, zs1, color="r", linestyle="solid")
# plt.plot(xs, zs2, color="g", linestyle="solid")
plt.plot(xs, zs3, color="r", linestyle="dotted")
plt.plot(xs, zs4, color="g", linestyle="dotted")


plt.show()
