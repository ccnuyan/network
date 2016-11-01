import networkx as nx
import numpy as np 

def generate(BIGN, M, MIU, DELTA, path):

    G = nx.barabasi_albert_graph(BIGN,M)

    names = G.nodes()

    rands = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=True)

    for x in names:
        G.node[x]['plainValue'] = DELTA * np.random.randn() + MIU
    nx.write_graphml(G,path)

generate(10000,1,0,1,'data/nw_gen_10000_1_0_1_sf.graphml')
generate(10000,2,0,1,'data/nw_gen_10000_2_0_1_sf.graphml')
generate(10000,3,0,1,'data/nw_gen_10000_3_0_1_sf.graphml')
generate(10000,4,0,1,'data/nw_gen_10000_4_0_1_sf.graphml')
generate(10000,5,0,1,'data/nw_gen_10000_5_0_1_sf.graphml')

