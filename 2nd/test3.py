import numpy as np 
from scipy.stats import norm

count = 100
sum = 0

for i in range(1,count,1):

    vx = np.random.randn()
    vy = np.random.randn()

    # print(vx)
    # print(vy)
    prob = 1 / ( np.power(np.e,np.abs(vx*vx)/2) * np.power(2*np.pi,1/2) ) - norm.cdf(-vx)*vx
    
    # if prob < 0:
    print('vx:')
    print(vx)
    print('prob:')
    print(prob)

    # print('----')