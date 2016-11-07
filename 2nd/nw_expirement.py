import matplotlib.pyplot as plt
import networkx as nx


def compute(C, path):

    G = nx.read_graphml(path)

    count = 0

    ccdfx = [0]
    ccdfy1 = [0]
    ccdfy2 = [0]
    ccdfy3 = [1]
    ccdfy4 = [1]

    while count < 10:
        for x in G.nodes():
            neighborsHigher = 0
            neighborsPlainHigher = 0
            higherNodesValues = 0
            higherNodesPlainValues = 0

            for node in G.neighbors(x):
                if G.node[node]['value'] > G.node[x]['value']:
                    neighborsHigher += 1
                    higherNodesValues += G.node[node]['value']

                if G.node[node]['plainValue'] > G.node[x]['plainValue']:
                    neighborsPlainHigher += 1
                    higherNodesPlainValues += G.node[node]['plainValue']

            if neighborsHigher == 0:
                G.node[x]['newValue'] = G.node[x]['value']
            else:
                G.node[x]['newValue'] = higherNodesValues / neighborsHigher

            if neighborsPlainHigher == 0:
                G.node[x]['newPlainValue'] = G.node[x]['plainValue']
            else:
                G.node[x]['newPlainValue'] = higherNodesPlainValues / neighborsPlainHigher

        count += 1
        vsum = 0
        pvsum = 0
        v2sum = 0
        pv2sum = 0

        for x in G.nodes():
            G.node[x]['value'] = G.node[x]['newValue']
            G.node[x]['plainValue'] = G.node[x]['newPlainValue']

            vsum += G.node[x]['value']
            pvsum += G.node[x]['plainValue']

            v2sum += G.node[x]['value']*G.node[x]['value']/G.number_of_nodes()
            pv2sum += G.node[x]['plainValue']*G.node[x]['plainValue']/G.number_of_nodes()

        ccdfx.append(count)
        ccdfy1.append(vsum/G.number_of_nodes())
        ccdfy2.append(pvsum/G.number_of_nodes())

        ccdfy3.append(v2sum - (vsum/G.number_of_nodes())*vsum/G.number_of_nodes())
        ccdfy4.append(pv2sum - (pvsum/G.number_of_nodes())*pvsum/G.number_of_nodes())

    return (ccdfx, ccdfy1, ccdfy2, ccdfy3, ccdfy4)

# ret1 = compute(0.1,"data/test.graphml")
ret1 = compute(0.01, "data/nw_gen_2_norm.graphml")
# ret1 = compute(0.01,"data/nw_gen_2_norm.graphml")

plt.plot(ret1[0], ret1[1], 'r', marker='o')
plt.plot(ret1[0], ret1[2], 'g', marker='o')
plt.plot(ret1[0], ret1[3], 'r', marker='*', linestyle='dashed')
plt.plot(ret1[0], ret1[4], 'g', marker='*', linestyle='dashed')


plt.title("nth step - average")
plt.ylabel("average")
plt.xlabel("nth step")

# draw graph in inset
plt.axes([0.45, 0.45, 0.45, 0.45])
# Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
# pos=nx.spring_layout(Gcc)
plt.axis('off')
# nx.draw_networkx_nodes(Gcc,pos,node_size=20)
# nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

plt.savefig("nth step - average.png")
plt.show()

#"data/nw_gen_10000_1.graphml"
