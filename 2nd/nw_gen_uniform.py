import networkx as nx
import numpy as np

from computeByAssumtion import compute


def generate(BIGN, M, path):

    L = [x for x in range(0, BIGN, 1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    names = G.nodes()

    rands = np.arange(1, -1, -2/BIGN)

    compute(G, M, rands, names, path)

N_POINTS = 10000

generate(N_POINTS, 2, 'data/nw_gen_1_uniform.graphml')
generate(N_POINTS, 10, 'data/nw_gen_2_uniform.graphml')
# generate(N_POINTS, 3, 'data/nw_gen_3_uniform.graphml')
