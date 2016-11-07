import networkx as nx
import scipy.stats as stats

from computeByAssumtion import compute


def generate(BIGN, M, a, b, path):

    L = [x for x in range(0, BIGN, 1)]

    G = nx.Graph()

    G.add_nodes_from(L)

    names = G.nodes()

    rands = stats.beta.rvs(a=a, b=b, size=BIGN)
    
    compute(G, M, rands, names, path)

N_POINTS = 10000

generate(N_POINTS, 2, 0.5, 0.5, 'data/nw_gen_1_beta.graphml')
generate(N_POINTS, 10, 0.5, 0.5, 'data/nw_gen_2_beta.graphml')
# generate(N_POINTS, 3, 0.5, 0.5, 'data/nw_gen_3_beta.graphml')
