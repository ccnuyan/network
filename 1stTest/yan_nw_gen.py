import networkx as nx
import numpy as np 

# NODES
BIGN = 100


G = nx.barabasi_albert_graph(BIGN,2)
dgs = nx.degree(G)


L = [x for x in range(0,BIGN,1)]
S = (30 * np.random.randn(BIGN) + 100).tolist()

scores = dict(zip(L, S))

nx.set_node_attributes(G, 'degree', dgs)
nx.set_node_attributes(G, 'score', scores)


# this could be displayed by gephi
nx.write_graphml(G,'yan_nw_gen.graphml')

