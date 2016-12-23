'''
bayesian main
'''

import matplotlib.pyplot as plt
from bayesian_experiment import Experiment as Experiment

# EXP = Experiment({
#     'signal_true_probability':0.6,
#     'p_0_0':0.54,
#     'p_1_1':0.2
# })

EXP = Experiment({
    'signal_true_probability':0.8,
    'p_0_0':0.7,
    'p_1_1':0.15
})

# EXP = Experiment({
#     'signal_true_probability':0.6,
#     'p_0_0':0.54,
#     'p_1_1':0.38
# })

STEPS = 10000
COUNT = 0

while COUNT < STEPS:
    EXP.get_signal()
    EXP.update()
    COUNT += 1

EXP.condition_check()
plt.plot(EXP.history0, color='g')
plt.plot(EXP.history1, color='r')
plt.show()
