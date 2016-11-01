import networkx as nx
import numpy as np 
import math as math
import itertools as itertools

def generate(BIGN, M, MIU, DELTA, path):
    L = [x for x in range(0,BIGN,1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    names = G.nodes()

    sum = 0

    rands = sorted(DELTA * np.random.randn(BIGN) + MIU, reverse=True)

    for x in names:
        G.node[x]['value'] = float(rands[x])
        G.node[x]['plainValue'] = DELTA * np.random.randn() + MIU
        G.node[x]['floor'] = float(sum)
        sum += rands[x]
        G.node[x]['ceil'] = float(sum)

    edgeCount = 0

    its = itertools.permutations(range(0,M+1,1),2)

    for it in its:
        G.add_edge(it[0],it[1])

    # each nodes
    for x in names:
        
        if x<M+1:
            continue;

        count = 0
        
        # each link
        while count < M:
            
            # generate a random number


            potentialLink = 0

            flag = False

            for y in names:
        
                if y>=x:                
                    break
        
                randsum = G.node[x]['ceil'] - x*G.node[x]['value']
                rand = np.random.rand()*randsum

                floor = G.node[y]['floor']-y*G.node[x]['value']
                ceil = G.node[y]['ceil']-(y+1)*G.node[x]['value']
                
                if rand>floor and rand<ceil:
                    if y in G.neighbors(x):
                        continue
                    else:
                        flag = True
                        potentialLink = y
                        break

            if not flag:
                continue 
            else:
                edgeCount += 1  
                count += 1              
                G.add_edge(x,potentialLink)
    nx.write_graphml(G,path)

generate(10000,1,0,1,'data/nw_gen_10000_1_0_1_0.graphml')
generate(10000,2,0,1,'data/nw_gen_10000_2_0_1_0.graphml')
generate(10000,3,0,1,'data/nw_gen_10000_3_0_1_0.graphml')
generate(10000,4,0,1,'data/nw_gen_10000_4_0_1_0.graphml')
generate(10000,5,0,1,'data/nw_gen_10000_5_0_1_0.graphml')