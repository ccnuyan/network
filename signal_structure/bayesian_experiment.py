'''
experiment
'''

import scipy.stats as stats


class Experiment(object):
    '''
    Experiment
    '''

    def __init__(self, params):

        # real world signal structure, agents don't know
        self.true_state = 0
        self.signal_true_probability = params['signal_true_probability']

        # personal signal structure
        # p_signal_state
        self.p_0_0 = params['p_0_0']
        self.p_1_0 = 1 - self.p_0_0
        self.p_1_1 = params['p_1_1']
        self.p_0_1 = 1 - self.p_1_1

        self.history1 = []
        self.history0 = []

        self.signal = 0
        self.signals = []

        self.prior0 = 1 / 2
        self.prior1 = 1 / 2

    def __str__(self):
        return 'Experiment'

    def get_signal(self):
        '''
        signal generator
        '''
        rand = stats.uniform.rvs(loc=0, scale=1)

        if rand < self.signal_true_probability:
            self.signal = self.true_state
        else:
            self.signal = 1 - self.true_state

        self.signals.append(self.signal)

    def update(self):
        '''
        compute likelihood
        '''

        self.history1.append(self.prior1)
        self.history0.append(self.prior0)

        if self.signal == 1:
            p_1 = self.p_1_0 * self.prior0 + self.p_1_1 * self.prior1
            post1 = self.p_1_1 * self.prior1 / p_1
            post0 = self.p_1_0 * self.prior0 / p_1

        if self.signal == 0:
            p_0 = self.p_0_0 * self.prior0 + self.p_0_1 * self.prior1
            post1 = self.p_0_1 * self.prior1 / p_0
            post0 = self.p_0_0 * self.prior0 / p_0

        self.prior1 = post1
        self.prior0 = post0

    def condition_check(self):
        '''condition check'''

        a = self.p_1_0
        b = self.p_0_1
        d = self.signal_true_probability

        cond0 = (1 - a - b) * (d - b)
        cond1 = (1 - a - b) * (a + d - 1)

        # factors = (1 - a - b) * (d - b - r * (1 - a - b))
        # diff = cond0 - cond1 = (1 - a - b) * (1 - a - b) > 0
        # so cond0 > cond1

        # a:p10, b:p01 d:p0

        print('(1 - a - b):%s' % (1 - a - b))
        print('(1 - a - b) * (d - b):%s' % cond0)
        print('(1 - a - b) * (a + d - 1):%s' % cond1)

        if cond1 > 0:
            return True
        if cond0 < 0:
            return False
        if cond1 < 0 and cond0 > 0:
            return True
