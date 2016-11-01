import networkx as nx
import numpy as np 
import math as math
import itertools as itertools
from scipy.stats import norm


def generate(BIGN, M, MIU, DELTA, path):
    L = [x for x in range(0,BIGN,1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    names = G.nodes()

    count = 0

    C = (BIGN-1)*np.power(2*np.pi,-0.5)

    rands = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=True)

    for x in names:
        G.node[x]['value'] = float(rands[x])
        G.node[x]['plainValue'] = DELTA * np.random.randn() + MIU


    for x in names:
        vx = G.node[x]['value']
        fm = C*np.power(np.e,-0.5*np.abs(vx*vx)) - (BIGN-1)*norm.cdf(-vx)*vx

        for y in names:
            if x==y or vx>G.node[y]['value']:
                continue
            vy = G.node[y]['value']
            
            rand1 = np.random.rand()

            fz = np.abs(vx-vy)

            rand2 = fz*M / (fm + fz)

            if rand1<rand2:
                G.add_edge(x,y)
                count += 1
    print(count)
    nx.write_graphml(G,path)


generate(10000,1,0,1,'data/nw_gen_10000_1_0_1_1.graphml')
generate(10000,2,0,1,'data/nw_gen_10000_2_0_1_1.graphml')
generate(10000,3,0,1,'data/nw_gen_10000_3_0_1_1.graphml')
generate(10000,4,0,1,'data/nw_gen_10000_4_0_1_1.graphml')
generate(10000,5,0,1,'data/nw_gen_10000_5_0_1_1.graphml')