import numpy as np 
from scipy.stats import norm

BIGN = 1000000

rands = np.random.randn(BIGN)

sum = 0
count = 0

cut = 1

for rand in rands:
    if(rand>cut):
        sum += rand
        count += 1

print(sum)
print(count)
print(sum/count)

# very impressive result
print((1/(np.power(2*np.pi,1/2)*norm.cdf(-cut)))*(np.power(np.e,-cut*cut/2)))




