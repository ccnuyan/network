import networkx as nx
import matplotlib.pyplot as plt

def drawdd(path,color,marker):
    G=nx.read_graphml(path)

    # A = nx.adjacency_matrix(G)
    # print(A.todense())

    # print("radius: %d" % nx.radius(G))
    # print("diameter: %d" % nx.diameter(G))
    # print("eccentricity: %s" % nx.eccentricity(G))
    # print("center: %s" % nx.center(G))
    # print("periphery: %s" % nx.periphery(G))
    # print("density: %s" % nx.density(G))

    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
    # print "Degree sequence", degree_sequence
    dmax=max(degree_sequence)

    sum = 0

    ccdfx = []
    ccdfy = []

    dset = sorted(set(degree_sequence))

    for item in dset:
        ccdfx.append(item)
        ccdfy.append(degree_sequence.count(item))
        
    plt.loglog(ccdfx,ccdfy,color=color,marker=marker)

# drawdd("ykt/data.graphml",'r','o')
# plt.savefig("ykt/data.graphml.png")


# drawdd("data/nw_gen_10000_1_0_1_sf.graphml",'r','o')
# drawdd("data/nw_gen_10000_2_0_1_sf.graphml",'g','o')
# drawdd("data/nw_gen_10000_3_0_1_sf.graphml",'b','o')
# drawdd("data/nw_gen_10000_4_0_1_sf.graphml",'y','o')
# drawdd("data/nw_gen_10000_5_0_1_sf.graphml",'c','o')
# plt.savefig("degree_histogram_sf.png")


# drawdd("data/nw_gen_10000_1_0_1_0.graphml",'r','o')
# drawdd("data/nw_gen_10000_2_0_1_0.graphml",'g','o')
# drawdd("data/nw_gen_10000_3_0_1_0.graphml",'b','o')
# drawdd("data/nw_gen_10000_4_0_1_0.graphml",'y','o')
# drawdd("data/nw_gen_10000_5_0_1_0.graphml",'c','o')
# plt.savefig("degree_histogram_0.png")


# drawdd("data/nw_gen_10000_1_0_1_1.graphml",'r','o')
# drawdd("data/nw_gen_10000_2_0_1_1.graphml",'g','o')
# drawdd("data/nw_gen_10000_3_0_1_1.graphml",'b','o')
# drawdd("data/nw_gen_10000_4_0_1_1.graphml",'y','o')
# drawdd("data/nw_gen_10000_5_0_1_1.graphml",'c','o')
# plt.savefig("degree_histogram_1.png")


plt.title("Degree distribution plot")
plt.ylabel("number")
plt.xlabel("degree")

# draw graph in inset
plt.axes([0.45,0.45,0.45,0.45])
# Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
# pos=nx.spring_layout(Gcc)
plt.axis('off')
# nx.draw_networkx_nodes(Gcc,pos,node_size=20)
# nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

plt.show()