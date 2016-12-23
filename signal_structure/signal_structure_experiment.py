'''
moudle Experiment
'''

import math
import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats
import numpy as np


class Experiment(object):
    '''
    Experiment Class
    '''

    def __init__(self, params):
        self.points = params['points']
        self.density = params['density']

        self.random_links = params['random_links']
        self.cfd_radius = params['cfd_radius']
        self.omega = params['omega']
        self.steps = 0
        self.true_state = params['true_state']
        self.signal_true_probability = params['tp']
        self.informed = params['informed']
        self.middle = params['middle']
        self.uninformed = params['uninformed']

        self.p_i_1_1 = params['p_i_1_1']
        self.p_i_0_0 = params['p_i_0_0']
        self.p_u_1_1 = params['p_u_1_1']
        self.p_u_0_0 = params['p_u_0_0']
        self.p_m_1_1 = params['p_m_1_1']
        self.p_m_0_0 = params['p_m_0_0']

        self.signal = 0
        self.signals = []

        self.graph = nx.erdos_renyi_graph(self.points, self.density)

    def __str___(self):
        return 'experiment of log-linear learning rule'

    def initialize_graph(self):
        '''initialize the graph and prepare the first loop'''

        rands = stats.uniform.rvs(loc=0, scale=1, size=self.points)

        count = 0
        for node in self.graph:
            gnode = self.graph.node[node]
            gnode['prior_thita0'] = rands[node]
            gnode['prior_thita1'] = 1 - rands[node]
            gnode['prior_ratio'] = (1 - rands[node]) / rands[node]

            gnode['post_thita0'] = gnode['prior_thita0']
            gnode['post_thita1'] = gnode['prior_thita1']
            gnode['post_ratio'] = gnode['prior_ratio']

            gnode['thita0History'] = []
            gnode['thita1History'] = []
            gnode['ratioHistory'] = []


            if count < self.informed:
                gnode['informed'] = True
            elif count < self.informed + self.middle:
                gnode['middle'] = True
            elif count < self.informed + self.middle + self.uninformed:
                gnode['uninformed'] = True

            count += 1

    def load(self):
        '''
        prepare data for operating
        '''

        self.steps += 1

        for node in self.graph:
            gnode = self.graph.node[node]
            gnode['thita0'] = self.graph.node[node]['post_thita0']
            gnode['thita1'] = self.graph.node[node]['post_thita1']
            gnode['ratio'] = self.graph.node[node]['post_ratio']

            gnode['thita0History'].append(gnode['thita0'])
            gnode['thita1History'].append(gnode['thita1'])
            gnode['ratioHistory'].append(gnode['ratio'])


    def likelyhood_function(self, node):
        '''
        also known as the signal structure
        '''
        p_0_0 = 0
        p_1_1 = 0
        p_0_1 = 0
        p_1_0 = 0

        prior0 = self.graph.node[node]['thita0']
        prior1 = self.graph.node[node]['thita1']

        if 'informed' in self.graph.node[node]:
            p_0_0 = self.p_i_0_0
            p_1_0 = 1 - self.p_i_0_0
            p_1_1 = self.p_i_1_1
            p_0_1 = 1 - self.p_i_1_1

        if 'middle' in self.graph.node[node]:
            p_0_0 = self.p_m_0_0
            p_1_0 = 1 - self.p_m_0_0
            p_1_1 = self.p_m_1_1
            p_0_1 = 1 - self.p_m_1_1

        if 'uninformed' in self.graph.node[node]:
            p_0_0 = self.p_u_0_0
            p_1_0 = 1 - self.p_u_0_0
            p_1_1 = self.p_u_1_1
            p_0_1 = 1 - self.p_u_1_1

        # print(p_0_0, p_1_0, p_1_1, p_0_1, prior0, prior1)

        if self.signal == 0:
            total = p_0_0 * prior0 + p_0_1 * prior1
            fc_0 = p_0_0 * prior0 / total
            fc_1 = p_0_1 * prior1 / total

        if self.signal == 1:
            total = p_1_0 * prior0 + p_1_1 * prior1
            fc_0 = p_1_0 * prior0 / total
            fc_1 = p_1_1 * prior1 / total

        return {'fc_0': fc_0, 'fc_1': fc_1}

    def clear_links(self):
        '''
        clear links
        '''

        to_be_removed = []
        for edge in self.graph.edges():
            to_be_removed.append(edge)
        self.graph.remove_edges_from(to_be_removed)

    def link_all_in_radius(self):
        '''
        link update rule
        '''

        if self.cfd_radius is None:
            return

        for node_s in self.graph:
            for node_t in self.graph:
                if node_t == node_s:
                    continue

                distance = abs(self.graph.node[node_s]['thita0']
                               - self.graph.node[node_t]['thita0'])

                if distance > self.cfd_radius:
                    if node_t in self.graph.neighbors(node_s):
                        self.graph.remove_edge(node_s, node_t)

                if distance < self.cfd_radius:
                    if node_t not in self.graph.neighbors(node_s):
                        self.graph.add_edge(node_s, node_t)
        return

    def link_randomly(self):
        '''
        add random links
        '''

        if self.random_links is None:
            return

        to_be_added = []
        for node_s in self.graph:
            count = 0
            while count < self.random_links:
                rand = math.floor(stats.uniform.rvs(
                    loc=0, scale=self.graph.number_of_nodes()))
                if rand == node_s:
                    continue
                if (node_s, rand) not in to_be_added and rand not in self.graph.neighbors(node_s):
                    to_be_added.append((str(node_s), str(rand)))
                    count += 1

        self.graph.add_edges_from(to_be_added)

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

    def update_pl(self):
        '''
        realization of learning rule
        '''

        self.learning_rule = 'pl'

        signal = self.get_signal()

        for node in self.graph:

            mit = self.likelyhood_function(node)

            # for thita0
            # none_bayesian part
            none_bayesian0 = self.graph.node[node]['thita0']

            for peer in self.graph.neighbors(node):
                none_bayesian0 += self.graph.node[peer]['thita0']

            none_bayesian0 = none_bayesian0 / \
                (1 + len(self.graph.neighbors(node)))

            bayesian0 = mit['fc_0']
            self.graph.node[node]['post_thita0'] = (
                self.omega * bayesian0) + ((1 - self.omega) * none_bayesian0)

            # for thita1
            # none_bayesian part
            none_bayesian1 = self.graph.node[node]['thita1']

            for peer in self.graph.neighbors(node):
                none_bayesian1 += self.graph.node[peer]['thita1']

            none_bayesian1 = none_bayesian1 / \
                (1 + len(self.graph.neighbors(node)))

            bayesian1 = mit['fc_1']
            self.graph.node[node]['post_thita1'] = (
                self.omega * bayesian1) + ((1 - self.omega) * none_bayesian1)

    def update_ll(self):
        '''
        realization of log-linear learning rule
        '''

        self.learning_rule = 'll'

        signal = self.get_signal()

        for node in self.graph:

            gnode = self.graph.node[node]

            mit = self.likelyhood_function(node)

            # two part nbsp and nbnp
            nbsp = np.log(gnode['ratio'])

            nbnp = nbsp

            for peer in self.graph.neighbors(node):
                peer = self.graph.node[peer]
                nbnp += np.log(peer['ratio'])

            # nbnp contains the node itself
            nbnp = nbnp / (len(self.graph.neighbors(node)) + 1)

            nbp = 0

            if self.omega is None:
                nbp = nbnp
            else:
                nbp = (1 - self.omega) * nbsp + self.omega * nbnp

            eratio = 0

            bayesian_part = np.log(mit['fc_1']) - np.log(mit['fc_0'])
            eratio = bayesian_part + nbp

            if eratio > np.log(1000):
                eratio = np.log(1000)
            if eratio < -np.log(1000):
                eratio = -np.log(1000)

            ratio = np.exp(eratio)
            gnode['post_ratio'] = ratio
            gnode['post_thita0'] = 1 / (1 + ratio)
            gnode['post_thita1'] = ratio / (1 + ratio)

    def draw_thita(self, number, show):
        '''
        plot
        '''

        # fig = plt.figure(0)
        plt.title('Beliefs of state %s' % number)
        plt.xlabel('steps')

        for node in self.graph:
            count = 1
            x_axis = []
            y_axis = []
            for data in self.graph.node[node]['thita%sHistory' % number]:
                # if 'informed' in self.graph.node[node]:
                #     continue
                x_axis.append(count)
                y_axis.append(data)
                count += 1

            if 'informed' in self.graph.node[node]:
                plt.plot(x_axis, y_axis, linestyle='dotted', color='g')
            if 'middle' in self.graph.node[node]:
                plt.plot(x_axis, y_axis, linestyle='dotted', color='b')
            if 'uninformed' in self.graph.node[node]:
                plt.plot(x_axis, y_axis, linestyle='dotted', color='r')

        plt.savefig('t%(number)s-%(learning_rule)s-%(steps)s%(cfd_radius)'
                    's%(omega)s%(tp)s_%(pi00)s%(pi11)s%(pu00)s%(pu11)s.png' %
                    {
                        'number': number,
                        'cfd_radius': '_r-' + str(self.cfd_radius) if self.cfd_radius is not None else '',
                        'omega': '_omg-' + str(self.omega),
                        'steps': '_st-' + str(self.steps),
                        'tp': '_tp-' + str(self.signal_true_probability),
                        'pi00': '_pi00-' + str(self.p_i_0_0),
                        'pi11': '_pi11-' + str(self.p_i_1_1),
                        'pu00': '_pu00-' + str(self.p_u_0_0),
                        'pu11': '_pu11-' + str(self.p_u_1_1),
                        'learning_rule': self.learning_rule
                    })
        if show:
            plt.show()
        else:
            plt.close('all')


    def show_degree_sequence(self, show):
        '''
        show_degree_sequence
        '''

        fig = plt.figure(0)
        degree_sequence = sorted(
            nx.degree(self.graph).values(), reverse=True)  # degree sequence

        ccdfx = []
        ccdfy = []

        dset = sorted(set(degree_sequence))

        for item in dset:
            ccdfx.append(item)
            ccdfy.append(degree_sequence.count(item))

        plt.plot(ccdfx, ccdfy)

        plt.savefig('dd_radius' + str(self.cfd_radius) +
                    '_omega' + str(self.omega) + ".png")

        if show:
            plt.show()
        else:
            plt.close('all')

    def draw_ratio(self,show):
        '''
        plot
        '''

        # fig = plt.figure(0)
        plt.title('Belief ratio of state %s')
        plt.xlabel('steps')

        for node in self.graph:
            count = 1
            x_axis = []
            y_axis = []
            for data in self.graph.node[node]['ratioHistory']:
                # if 'informed' in self.graph.node[node]:
                #     continue
                x_axis.append(count)
                y_axis.append(data)
                count += 1

            if 'informed' in self.graph.node[node]:
                plt.semilogy(x_axis, y_axis, linestyle='dotted', color='g')
            if 'middle' in self.graph.node[node]:
                plt.semilogy(x_axis, y_axis, linestyle='dotted', color='b')
            if 'uninformed' in self.graph.node[node]:
                plt.semilogy(x_axis, y_axis, linestyle='dotted', color='r')

        plt.savefig('ratio-%(learning_rule)s-%(steps)s%(cfd_radius)'
                    's%(omega)s%(tp)s_%(pi00)s%(pi11)s%(pu00)s%(pu11)s.png' %
                    {
                        'cfd_radius': '_r-' + str(self.cfd_radius) if self.cfd_radius is not None else '',
                        'omega': '_omg-' + str(self.omega),
                        'steps': '_st-' + str(self.steps),
                        'tp': '_tp-' + str(self.signal_true_probability),
                        'pi00': '_pi00-' + str(self.p_i_0_0),
                        'pi11': '_pi11-' + str(self.p_i_1_1),
                        'pu00': '_pu00-' + str(self.p_u_0_0),
                        'pu11': '_pu11-' + str(self.p_u_1_1),
                        'learning_rule': self.learning_rule
                    })
        if show:
            plt.show()
        else:
            plt.close('all')