import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def pxofk(alpha, xmin, k):
    px = (alpha - 1) / xmin * np.power(k / xmin, -alpha)
    return px

def estimate(G, Min):
    degrees = G.degree()
    total = 0
    count = 0

    for x in G.nodes():
        if degrees[x] > Min:
            count += 1
            total += np.log(degrees[x]/Min)

    return 1 + count * (1 / total)

def kstest(min, path):

    G = nx.read_graphml(path)
    degree_sequence = sorted(nx.degree(G).values(), reverse=True)

    dset = sorted(set(degree_sequence))

    ds = {}

    for item in dset:
        ds[item] = degree_sequence.count(item)

    xmin = min

    alphas = {}

    while xmin in ds.keys():
        alpha = estimate(G, xmin)

        diffmax = 0

        sumofx = 0

        for k in ds.keys():
            if k > xmin:
                sumofx += ds[k]

        for k in dset:
            diff = np.abs(ds[k]/sumofx - pxofk(alpha, xmin, k))
            if diffmax < diff:
                diffmax = diff

        alphas[xmin] = {'alpha':alpha, 'diff':diffmax}
        xmin += 1

    return alphas

# alpha = estimate(2, "data/nw_gen_1_norm.graphml")

ret = kstest(2, "data/nw_gen_1_norm.graphml")

diffx = 0
mkey = 0
for key in ret.keys():
    if diffx == 0:
        mkey = key
        diffx = ret[key]['diff']
    elif ret[key]['diff'] < diffx:
        diffx = ret[key]['diff']
        mkey = key

print(ret)
print(mkey)
print(ret[mkey])
# print(alpha)
