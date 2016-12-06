import matplotlib.pyplot as plt
import scipy.stats as stats

u = 0.3
count = 0

xAxis = []
yAxis = []

steps = 1000

while count < steps:
    xAxis.append(count)
    yAxis.append(u)

    rand = stats.uniform.rvs(loc=0, scale=1)

    signal = ''

    if rand < 0.7:
        signal = 'H'
    else:
        signal = 'T'

    if signal == 'H':
        u = u * 0.8 / (0.8 * u + 0.2 * (1 - u))
    if signal == 'T':
        u = u * 0.2 / (0.8 * (1 - u) + 0.2 * u)

    count += 1

fig = plt.figure(0)
plt.title("Bayesian Test")

plt.semilogx(xAxis, yAxis)
plt.savefig('BayesianTest')
plt.close('all')
