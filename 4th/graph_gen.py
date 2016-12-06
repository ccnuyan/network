import math
import networkx as nx
import numpy as np
import scipy.stats as stats

def generate(BIGN, bottom, top, informed, path):

    L = [x for x in range(0, BIGN, 1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    oldrands = stats.uniform.rvs(loc=bottom, scale=top, size=BIGN)

    rands = sorted(oldrands, reverse=False)

    data = [(l, {'prior_thita1': float(rands[l]), 'prior_thita2': (1- float(rands[l]))}) for l in L]

    G.add_nodes_from(data)

    number_of_nodes = G.number_of_nodes()
    count = 0
    while informed > count:
        randIndex = math.floor(stats.uniform.rvs(loc=0, scale=number_of_nodes))
        if 'informed' in G.node[randIndex]:
            continue
        else:
            count += 1
            G.node[randIndex]['informed'] = True

    nx.write_graphml(G, path)

N_POINTS = 100
Informed = 100

generate(N_POINTS, 0, 1, Informed, 'data/uniform_' + str(Informed) + 'in' + str(N_POINTS) + 'informed.graphml')
