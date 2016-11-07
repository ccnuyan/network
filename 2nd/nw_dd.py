import networkx as nx
import matplotlib.pyplot as plt


def drawdd(path, color, marker, linestyle):
    G = nx.read_graphml(path)

    # A = nx.adjacency_matrix(G)
    # print(A.todense())

    # print("radius: %d" % nx.radius(G))
    # print("diameter: %d" % nx.diameter(G))
    # print("eccentricity: %s" % nx.eccentricity(G))
    # print("center: %s" % nx.center(G))
    # print("periphery: %s" % nx.periphery(G))
    # print("density: %s" % nx.density(G))

    degree_sequence = sorted(nx.degree(G).values(), reverse=True) # degree sequence
    # print "Degree sequence", degree_sequence
    # dmax=max(degree_sequence)

    ccdfx = []
    ccdfy = []

    dset = sorted(set(degree_sequence))

    for item in dset:
        ccdfx.append(item)
        ccdfy.append(degree_sequence.count(item))

    plt.loglog(ccdfx, ccdfy, color=color, marker=marker, linestyle=linestyle)

# drawdd("ykt/data.graphml", 'r', 'o')
# plt.savefig("ykt/data.graphml.png")

# drawdd("data/nw_gen_1_sf.graphml", 'black', '+', 'solid')
# drawdd("data/nw_gen_2_sf.graphml", 'black', 'x', 'solid')

drawdd("data/nw_gen_1_norm.graphml", 'r', '+', 'dotted')
drawdd("data/nw_gen_2_norm.graphml", 'r', 'x', 'dashdot')

drawdd("data/nw_gen_1_uniform.graphml", 'g', '+', 'dotted')
drawdd("data/nw_gen_2_uniform.graphml", 'g', 'x', 'dotted')

drawdd("data/nw_gen_1_bn.graphml", 'b', '+', 'dotted')
drawdd("data/nw_gen_2_bn.graphml", 'b', 'x', 'dotted')

drawdd("data/nw_gen_1_ps.graphml", 'pink', '+', 'dotted')
drawdd("data/nw_gen_2_ps.graphml", 'pink', 'x', 'dotted')

drawdd("data/nw_gen_1_expon.graphml", 'cyan', '+', 'dotted')
drawdd("data/nw_gen_2_expon.graphml", 'cyan', '+', 'dotted')

# drawdd("data/nw_gen_1_beta.graphml", 'r', '+')
# drawdd("data/nw_gen_2_beta.graphml", 'g', '+')

plt.title("Degree distribution plot")
plt.ylabel("number")
plt.xlabel("degree")

# draw graph in inset
plt.axes([0.45, 0.45, 0.45, 0.45])
# Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
# pos=nx.spring_layout(Gcc)
plt.axis('off')
# nx.draw_networkx_nodes(Gcc,pos,node_size=20)
# nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

plt.show()
