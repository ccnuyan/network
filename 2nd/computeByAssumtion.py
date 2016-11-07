import itertools

import networkx as nx
import numpy as np


def compute(G, M, oldrands, names, path):
    total = 0

    rands = sorted(oldrands, reverse=True)

    # values in rands decrease
    for x in names:
        G.node[x]['value'] = float(rands[x])
        G.node[x]['floor'] = float(total)
        total += rands[x]
        G.node[x]['ceil'] = float(total)
        G.node[x]['overflow'] = float(total - (x+1)*rands[x])

        G.node[x]['plainValue'] = float(oldrands[x])
        # print(G.node[x])

    # add the links between high valued points to make a complete subnetwork
    its = itertools.combinations(range(0, M+1, 1), 2)

    for it in its:
        # print(str(it[0]) + '-' + str(it[1]))
        G.add_edge(it[0], it[1])

    count = int((M+1)*M/2)

    # each nodes
    for x in names:

        # already a complete network
        if x < (M+1):
            continue

        # each link
        # generate a random number
        nodeCount = 0
        while nodeCount < M:
            rand = np.random.rand() * G.node[x]['overflow']

            for y in names:
                if y >= x:
                    break
                if G.node[x]['value'] == G.node[y]['value']:
                    break
                if y in G.neighbors(x):
                    continue

                floor = G.node[y]['floor'] - y*G.node[x]['value']
                ceil = G.node[y]['ceil'] - (y+1)*G.node[x]['value']
                if floor <= rand and rand <= ceil:
                    count += 1
                    nodeCount += 1
                    G.add_edge(x, y)
                    break

    print(count)
    nx.write_graphml(G, path)
