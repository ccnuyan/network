import json
import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats

u = 0.3
count = 0

while count < 10:

    rand = stats.uniform.rvs(loc=0, scale=1)

    signal = ''

    if rand < 0.8:
        signal = 'H'
    else:
        signal = 'T'

    if signal == 'H':
        u = u*0.8/(0.8*u+0.2*(1-u))
    if signal == 'T':
        u = u*0.2/(0.8*(1-u)+0.2*u)

    print(u)

    count += 1