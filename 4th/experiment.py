import json
import math

import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats


class Experiment(object):
    def __init__(self, path, omega, link_s, link_d, cfd_radius, likelyhood_function=None, forcast_function=None, signal_possibility=None):
        self.path = path
        self.omega = omega
        self.cfd_radius = cfd_radius
        self.link_s = link_s
        self.link_d = link_d

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
        return 'experiment 5'

    def link(self):
        to_be_removed = []
        for edge in self.G.edges():
            to_be_removed.append(edge)
        self.G.remove_edges_from(to_be_removed)

        toBeAdded = []

        # in radius

        if self.link_s != 0 and self.cfd_radius != 0:
            for node_s in self.G:

                nodes_in_radius = []

                for node_t in self.G:
                    if node_t == node_s:
                        continue
                    distance = abs(self.G.node[node_s]['thita1'] - self.G.node[node_t]['thita1'])
                    if distance < self.cfd_radius and node_t not in self.G.neighbors(node_s):
                        nodes_in_radius.append(node_t)

                count = 0
                if len(nodes_in_radius) > self.link_s:
                    while count < self.link_s:
                        rand = math.floor(stats.uniform.rvs(loc=0, scale=len(nodes_in_radius)))
                        if (node_s, nodes_in_radius[rand]) not in toBeAdded and nodes_in_radius[rand] not in self.G.neighbors(node_s):
                            toBeAdded.append((node_s, nodes_in_radius[rand]))
                            count += 1
                else:
                    toBeAdded.extend([(node_s, node) for node in nodes_in_radius])

        if self.link_d != 0:
            for node_s in self.G:
                cdf = []
                floor = 0
                ceil = 0
                for node_t in self.G:
                    if node_t == node_s:
                        continue

                    ceil += abs(self.G.node[node_t]['thita1'] - self.G.node[node_s]['thita1'])
                    cdf.append({'id': node_t, 'floor': floor, 'ceil': ceil})
                    floor = ceil

                count = 0
                while count < self.link_d:
                    rand = stats.uniform.rvs(loc=0, scale=ceil)
                    for interium in cdf:
                        if (node_s, interium['id']) not in toBeAdded and interium['floor'] < rand and rand < interium['ceil']:
                            toBeAdded.append((node_s, interium['id']))
                            count += 1
                            break
        # print(toBeAdded)
        self.G.add_edges_from(toBeAdded)
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


    def draw_thita1(self, show):
        plt.title("Beliefs of state 1")
        plt.ylabel("r=" + str(self.cfd_radius) + ' omega=' + str(self.omega))
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

            if 'informed' in self.G.node[node]:
                plt.semilogx(xAxis, yAxis, linestyle='solid', color='r')
            else:
                plt.semilogx(xAxis, yAxis, linestyle='dotted', color='b')

        plt.savefig('pngs/thita1_pts' + str(self.G.number_of_nodes()) + '_s' + str(self.link_s) + '_d' + str(self.link_d) + '_o' + str(self.omega) + '_r' + str(self.cfd_radius) + ".png")
        if show:
            plt.show()
        else:
            plt.close('all')

    def draw_thita2(self, show):
        plt.title("Beliefs of state 2")
        plt.ylabel("r=" + str(self.cfd_radius) + ' omega=' + str(self.omega))
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

            if 'informed' in self.G.node[node]:
                plt.semilogx(xAxis, yAxis, linestyle='solid', color='r')
            else:
                plt.semilogx(xAxis, yAxis, linestyle='dotted', color='b')

        plt.savefig('pngs/thita2_pts' + str(self.G.number_of_nodes()) + '_s' + str(self.link_s) + '_d' + str(self.link_d) + '_o' + str(self.omega) + '_r' + str(self.cfd_radius) + ".png")
        if show:
            plt.show()
        else:
            plt.close('all')

    def show_degree_sequence(self, show):
        degree_sequence = sorted(nx.degree(self.G).values(), reverse=True) # degree sequence

        ccdfx = []
        ccdfy = []

        dset = sorted(set(degree_sequence))

        for item in dset:
            ccdfx.append(item)
            ccdfy.append(degree_sequence.count(item))

        plt.loglog(ccdfx, ccdfy)

        plt.savefig('pngs/dd_points' + str(self.G.number_of_nodes()) + '_s' + str(self.link_s) + '_d' + str(self.link_d) + '_o' + str(self.omega) + '_r' + str(self.cfd_radius) + ".png")

        if show:
            plt.show()
        else:
            plt.close('all')

    def finalize(self):
        for node in self.G:
            self.G.node[node]['thita1History'] = json.dumps(self.G.node[node]['thita1History'])
            self.G.node[node]['thita2History'] = json.dumps(self.G.node[node]['thita2History'])

        nx.write_graphml(self.G, 'end.graphml')
