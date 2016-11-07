import networkx as nx
import scipy.stats as stats

from computeByAssumtion import compute


def generate(BIGN, M, mu, loc, path):

    L = [x for x in range(0, BIGN, 1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    names = G.nodes()

    rands = stats.binom.rvs(n=N, p=P, size=BIGN)

    compute(G, M, rands, names, path)

N_POINTS = 10000

generate(N_POINTS, 2, 2, 0, 'data/nw_gen_1_ps.graphml')
generate(N_POINTS, 10, 2, 0, 'data/nw_gen_2_ps.graphml')
# generate(N_POINTS, 3, 2, 0, 'data/nw_gen_3_ps.graphml')
