import numpy as np 
from scipy.stats import norm

count = 100
sum = 0

for i in range(1,count,1):

    vx = np.random.randn()
    vy = np.random.randn()

    # print(vx)
    # print(vy)
    prob = np.abs(vx-vy) * ( np.power(np.e,np.abs(vx*vy)/2) * np.power(2*np.pi,1/2) )
    sum += prob
    # print('----')

print(sum/count)