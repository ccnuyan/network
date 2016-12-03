import json
import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats


class Experiment(object):
    def __init__(self, path, cfd_radius, omega, likelyhood_function=None, forcast_function=None, signal_possibility=None):
        self.path = path
        self.cfd_radius = cfd_radius
        self.omega = omega

        self.G = nx.read_graphml(path)

        # signal structure
        if likelyhood_function is None:
            lf_threshold = 0.8
            def lf(thita, signal):
                if thita == 1 and signal == 'H':
                    return lf_threshold
                if thita == 2 and signal == 'T':
                    return lf_threshold
                if thita == 2 and signal == 'H':
                    return 1 - lf_threshold
                if thita == 1 and signal == 'T':
                    return 1 - lf_threshold

            self.likelyhood_function = lf
        else:
            self.likelyhood_function = likelyhood_function

        # signal forcast
        if forcast_function is None:
            def ff(node, signal):
                mit = node['thita1'] * self.likelyhood_function(1, signal) + node['thita2'] * self.likelyhood_function(2, signal)
                return mit
            self.forcast_function = ff
        else:
            self.forcast_function = forcast_function

        # signal possibility
        if signal_possibility is None:
            sp_threshold = 0.8
            self.signal_possibility = {'H': sp_threshold, 'T': 1 - sp_threshold}
        else:
            self.signal_possibility = signal_possibility

        # initialize
        for node in self.G:
            self.G.node[node]['thita1'] = self.G.node[node]['prior_thita1']
            self.G.node[node]['thita1History'] = [self.G.node[node]['thita1']]
            self.G.node[node]['thita2'] = self.G.node[node]['prior_thita2']
            self.G.node[node]['thita2History'] = [self.G.node[node]['thita2']]

    def __str___(self):
        return 'experiment'

    def link(self):
        for node_s in self.G:
            for node_t in self.G:
                if node_t == node_s:
                    continue

                distance = abs(self.G.node[node_s]['thita1'] - self.G.node[node_t]['thita1'])

                if distance > self.cfd_radius:
                    if node_t in self.G.neighbors(node_s):
                        self.G.remove_edge(node_s, node_t)

                if distance < self.cfd_radius:
                    if node_t not in self.G.neighbors(node_s):
                        self.G.add_edge(node_s, node_t)
        return

    def getSignal(self):
        rand = stats.uniform.rvs(loc=0, scale=1)

        signal = ''

        if rand < self.signal_possibility['H']:
            signal = 'H'
        else:
            signal = 'T'

        return signal

    def update(self):

        for node in self.G:

            signal = self.getSignal()

            mit = self.forcast_function(self.G.node[node], signal)

            # for thita1
            # none_bayesian part
            none_bayesian1 = self.G.node[node]['thita1']

            for peer1 in self.G.neighbors(node):
                none_bayesian1 += self.G.node[peer1]['thita1']

            none_bayesian1 = none_bayesian1 / (1 + len(self.G.neighbors(node)))

            # bayesian1 part
            if 'informed' in self.G.node[node]:
                bayesian1 = self.G.node[node]['thita1'] * self.likelyhood_function(1, signal) / mit
                self.G.node[node]['post_thita1'] = (self.omega * bayesian1) + ((1 - self.omega) *  none_bayesian1)
            else:
                self.G.node[node]['post_thita1'] = none_bayesian1

            # for thita2
            # none_bayesian part
            none_bayesian2 = self.G.node[node]['thita2']

            for peer2 in self.G.neighbors(node):
                none_bayesian2 += self.G.node[peer2]['thita2']

            none_bayesian2 = none_bayesian2 / (1 + len(self.G.neighbors(node)))

            # bayesian2 part
            if 'informed' in self.G.node[node]:
                bayesian2 = self.G.node[node]['thita2'] * self.likelyhood_function(2, signal) / mit
                self.G.node[node]['post_thita2'] = (self.omega * bayesian2) + ((1 - self.omega) *  none_bayesian2)
            else:
                self.G.node[node]['post_thita2'] = none_bayesian2

        for node in self.G:
            self.G.node[node]['thita1'] = self.G.node[node]['post_thita1']
            self.G.node[node]['thita2'] = self.G.node[node]['post_thita2']
            self.G.node[node]['thita1History'].append(self.G.node[node]['thita1'])
            self.G.node[node]['thita2History'].append(self.G.node[node]['thita2'])


    def draw_thita1(self):
        plt.title("Beliefs of state 1")
        plt.ylabel("r=0.3")
        plt.xlabel("steps")

        for node in self.G:
            count = 1
            xAxis = []
            yAxis = []
            for data in self.G.node[node]['thita1History']:
                # if 'informed' in self.G.node[node]:
                #     continue
                xAxis.append(count)
                yAxis.append(data)
                count += 1

            plt.semilogx(xAxis, yAxis)
        plt.savefig('thita1_radius' + str(self.cfd_radius) + '_omega' + str(self.omega) + ".png")
        plt.show()
    
    def draw_thita2(self):
        plt.title("Beliefs of state 2")
        plt.ylabel("r=0.3")
        plt.xlabel("steps")

        for node in self.G:
            count = 1
            xAxis = []
            yAxis = []
            for data in self.G.node[node]['thita2History']:
                # if 'informed' in self.G.node[node]:
                #     continue
                xAxis.append(count)
                yAxis.append(data)
                count += 1

            plt.semilogx(xAxis, yAxis)

        plt.savefig('thita2_radius' + str(self.cfd_radius) + '_omega' + str(self.omega) + ".png")
        plt.show()

    def finalize(self):
        for node in self.G:
            self.G.node[node]['thita1History'] = json.dumps(self.G.node[node]['thita1History'])
            self.G.node[node]['thita2History'] = json.dumps(self.G.node[node]['thita2History'])
