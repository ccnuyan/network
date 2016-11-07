import math
import matplotlib.pyplot as plt

import numpy as np

m=2
bign = 31
result=[]
for k in range(1,bign,1):
    sum = 0
    power = np.power(m,k)
    for l in range(0,k+1):
        sum = sum + power/(math.factorial(l)*math.factorial(k-l))
    result.append(np.power(np.e,-2*m)*sum)

print(result)
plt.loglog(range(1,bign,1),result,color='red',marker='*')
plt.show()

#this is possion not power law
