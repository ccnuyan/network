'''
this is graph generator
'''

import math
import networkx as nx
import scipy.stats as stats


def generate(number, bottom, top, informed, path):
    '''
    generate a grapth with informed agents
    '''

    uniform_list = [x for x in range(0, number, 1)]

    graph = nx.Graph()

    graph.add_nodes_from(uniform_list)

    oldrands = stats.uniform.rvs(loc=bottom, scale=top, size=number)

    rands = sorted(oldrands, reverse=False)

    data = [(l, {'prior_thita1': float(rands[l]),
                 'prior_thita2': (1 - float(rands[l]))}) for l in uniform_list]

    # data = [(l, {'prior_thita1': 0.5, 'prior_thita2': 0.5})
    #         for l in uniform_list]

    graph.add_nodes_from(data)

    number_of_nodes = graph.number_of_nodes()
    count = 0
    while informed > count:
        rand_index = math.floor(
            stats.uniform.rvs(loc=0, scale=number_of_nodes))
        if 'informed' in graph.node[rand_index]:
            continue
        else:
            count += 1
            graph.node[rand_index]['informed'] = True

    nx.write_graphml(graph, path)

N_POINTS = 100
INFORMED = 20

generate(N_POINTS, 0, 1, INFORMED, 'data/uniform_' +
         str(INFORMED) + 'in' + str(N_POINTS) + 'informed.graphml')
