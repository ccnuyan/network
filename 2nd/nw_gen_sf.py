import networkx as nx
import numpy as np

def generate(BIGN, M, MIU, DELTA, path):

    G = nx.barabasi_albert_graph(BIGN,M)

    names = G.nodes()

    rands = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=True)

    # for x in names:
    #     G.node[x]['plainValue'] = DELTA * np.random.randn() + MIU
    
    nx.write_graphml(G,path)

N_POINTS = 10000

generate(N_POINTS, 2, 0, 1, 'data/nw_gen_1_sf.graphml')
generate(N_POINTS, 10, 0, 1, 'data/nw_gen_2_sf.graphml')
# generate(N_POINTS, 3, 0, 1, 'data/nw_gen_3_sf.graphml')

