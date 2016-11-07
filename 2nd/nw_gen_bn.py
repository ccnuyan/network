import networkx as nx
import scipy.stats as stats

from computeByAssumtion import compute


def generate(BIGN, M, N, P, path):

    L = [x for x in range(0, BIGN, 1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    names = G.nodes()

    rands = stats.binom.rvs(n=N, p=P, size=BIGN)
    
    compute(G, M, rands, names, path)

N_POINTS = 10000

generate(N_POINTS, 2, 100, 0.2, 'data/nw_gen_1_bn.graphml')
generate(N_POINTS, 10, 100, 0.2, 'data/nw_gen_2_bn.graphml')
# generate(N_POINTS, 3, 100, 0.2, 'data/nw_gen_3_bn.graphml')
