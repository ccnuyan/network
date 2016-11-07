import networkx as nx
import scipy.stats as stats

from computeByAssumtion import compute


def generate(BIGN, M, MIU, DELTA, path):

    L = [x for x in range(0, BIGN, 1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    names = G.nodes()

    rands = stats.norm.rvs(loc=MIU, scale=DELTA, size=BIGN)

    compute(G, M, rands, names, path)

N_POINTS = 10000

# generate(N_POINTS, 2, 0, 1, 'data/nw_gen_1_norm.graphml')
# generate(N_POINTS, 10, 0, 1, 'data/nw_gen_2_norm.graphml')

generate(10, 2, 0, 1, 'data/test.graphml')
