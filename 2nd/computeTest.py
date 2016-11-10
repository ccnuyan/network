import networkx as nx
import numpy as np 
import math as math
import itertools as itertools
from computeByAssumtion import compute

L = [x for x in range(0, 6, 1)]

G = nx.Graph()

G.add_nodes_from(L)

names = G.nodes()
rands = [15, 13, 8, 7, 5, 2]

print(rands)

compute(G, 2, rands, names, 'test.graphml')
