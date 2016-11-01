import networkx as nx
import matplotlib.pyplot as plt

G=nx.read_graphml("yan_nw_gen.graphml")

A = nx.adjacency_matrix(G)
print(A.todense())

print("radius: %d" % nx.radius(G))
print("diameter: %d" % nx.diameter(G))
print("eccentricity: %s" % nx.eccentricity(G))
print("center: %s" % nx.center(G))
print("periphery: %s" % nx.periphery(G))
print("density: %s" % nx.density(G))