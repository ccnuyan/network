'''
moudle Experiment
'''

import json
import math
import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats
import numpy as np


class Experiment(object):
    '''
    Experiment Class
    '''

    def __init__(self, path, params):
        self.path = path

        self.cfd_radius = params['cfd_radius']
        self.random_links = params['random_links']

        self.omega = params['omega']
        self.steps = 0
        self.sph = params['sph']
        self.h_1 = params['h_1']
        self.h_2 = params['h_2']

        self.graph = nx.read_graphml(path)  # initialize from file.

        self.signal_possibility = {
            'H': self.sph, 'T': 1 - self.sph}

        for node in self.graph:
            self.graph.node[node]['post_thita1'] = self.graph.node[
                node]['prior_thita1']
            self.graph.node[node]['post_thita2'] = self.graph.node[
                node]['prior_thita2']
            self.graph.node[node]['thita1History'] = []
            self.graph.node[node]['thita2History'] = []

    def __str___(self):
        return 'experiment of log-linear learning rule'

    def load(self):
        '''
        prepare data for operating
        '''

        self.steps += 1

        for node in self.graph:
            self.graph.node[node]['thita1'] = self.graph.node[
                node]['post_thita1']
            self.graph.node[node]['thita2'] = self.graph.node[
                node]['post_thita2']
            self.graph.node[node]['thita1History'].append(
                self.graph.node[node]['thita1'])
            self.graph.node[node]['thita2History'].append(
                self.graph.node[node]['thita2'])

    def likelyhood_function(self, thita, signal):
        '''
        also known as the signal structure
        '''

        # p(H|1)
        if signal == 'H' and thita == 1:
            return self.h_1

        # p(T|1)
        if signal == 'T' and thita == 1:
            return 1 - self.h_1

        # p(H|2)
        if signal == 'H' and thita == 2:
            return self.h_2

        # p(T|2)
        if signal == 'T' and thita == 2:
            return 1 - self.h_2

    def forcast_function(self, node, signal):
        '''
        1 step signal forcast
        '''

        mit = node['thita1'] * self.likelyhood_function(
            1, signal) + node['thita2'] * self.likelyhood_function(2, signal)
        return mit

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

                distance = abs(self.graph.node[node_s]['thita1']
                               - self.graph.node[node_t]['thita1'])

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

        signal = ''

        if rand < self.signal_possibility['H']:
            signal = 'H'
        else:
            signal = 'T'

        return signal

    def update_pl(self):
        '''
        realization of learning rule
        '''
        self.learning_rule = 'pl'
        for node in self.graph:

            signal = self.get_signal()

            mit = self.forcast_function(self.graph.node[node], signal)

            # for thita1
            # none_bayesian part
            none_bayesian1 = self.graph.node[node]['thita1']

            for peer1 in self.graph.neighbors(node):
                none_bayesian1 += self.graph.node[peer1]['thita1']

            none_bayesian1 = none_bayesian1 / \
                (1 + len(self.graph.neighbors(node)))

            # bayesian1 part
            if 'informed' in self.graph.node[node]:
                bayesian1 = self.graph.node[node][
                    'thita1'] * self.likelyhood_function(1, signal) / mit
                self.graph.node[node]['post_thita1'] = (
                    self.omega * bayesian1) + ((1 - self.omega) * none_bayesian1)
            else:
                self.graph.node[node]['post_thita1'] = none_bayesian1

            # for thita2
            # none_bayesian part
            none_bayesian2 = self.graph.node[node]['thita2']

            for peer2 in self.graph.neighbors(node):
                none_bayesian2 += self.graph.node[peer2]['thita2']

            none_bayesian2 = none_bayesian2 / \
                (1 + len(self.graph.neighbors(node)))

            # bayesian2 part
            if 'informed' in self.graph.node[node]:
                bayesian2 = self.graph.node[node][
                    'thita2'] * self.likelyhood_function(2, signal) / mit
                self.graph.node[node]['post_thita2'] = (
                    self.omega * bayesian2) + ((1 - self.omega) * none_bayesian2)
            else:
                self.graph.node[node]['post_thita2'] = none_bayesian2

    def update_ll(self):
        '''
        realization of log-linear learning rule
        '''

        self.learning_rule = 'll'
        for node in self.graph:

            signal = self.get_signal()

            # two part nbsp and nbnp_
            nbsp = np.log(
                self.graph.node[node]['thita1'] / self.graph.node[node]['thita2'])
            nbnp_ = nbsp

            for peer1 in self.graph.neighbors(node):
                nbnp_ += np.log(self.graph.node[peer1][
                    'thita1']) - np.log(self.graph.node[peer1]['thita2'])

            # nbnp_ contains the node itself
            nbnp_ = nbnp_ \
                / (len(self.graph.neighbors(node)) + 1)

            nbp = 0

            if self.omega is None:
                nbp = nbnp_
            else:
                nbp = (1 - self.omega) * nbsp \
                    + self.omega * nbnp_

            eratio = 0

            if 'informed' in self.graph.node[node]:
                bayesian_part = np.log(self.likelyhood_function(
                    1, signal)) - np.log(self.likelyhood_function(2, signal))
                eratio = bayesian_part + nbp
            else:
                eratio = nbp

            ratio = np.exp(eratio)

            self.graph.node[node]['post_thita1'] = ratio / (1 + ratio)
            self.graph.node[node]['post_thita2'] = 1 / (1 + ratio)

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
                plt.plot(x_axis, y_axis, linestyle='dotted', color='r')
            else:
                plt.plot(x_axis, y_axis, linestyle='dotted', color='b')

        plt.savefig('t%(number)s-%(learning_rule)s-%(steps)s%(cfd_radius)s%(omega)s%(sph)s_h12-%(h_1)s-%(h_2)s.png' %
                    {
                        'number': number,
                        'cfd_radius': '_r-' + str(self.cfd_radius) \
                            if self.cfd_radius is not None else '',
                        'omega': '_omg-' + str(self.omega),
                        'steps': '_st-' + str(self.steps),
                        'sph': '_sph-' + str(self.sph),
                        'h_1': self.h_1,
                        'h_2': self.h_2,
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

    def finalize(self):
        '''
        save graph to file
        '''

        for node in self.graph:
            self.graph.node[node]['thita1History'] = json.dumps(
                self.graph.node[node]['thita1History'])
            self.graph.node[node]['thita2History'] = json.dumps(
                self.graph.node[node]['thita2History'])

        nx.write_graphml(self.graph, 'end.graphml')
