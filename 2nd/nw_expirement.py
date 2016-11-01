import networkx as nx
import matplotlib.pyplot as plt

def compute(C , path):

    G=nx.read_graphml(path)

    count = 0

    ccdfx = [0]
    ccdfy1 = [0]
    ccdfy2 = [0]

    while count < 100:

        for x in G.nodes():
            neighborsHigher = sum({(1 if G.node[node]['value']>G.node[x]['value'] else 0) for node in G.neighbors(x)});
            neighborsPlainHigher = sum({(1 if G.node[node]['plainValue']>G.node[x]['plainValue'] else 0) for node in G.neighbors(x)});
            
            if neighborsHigher == 0:
                G.node[x]['newValue'] = G.node[x]['value']
            else:
                G.node[x]['newValue'] = G.node[x]['value'] + C*sum({(G.node[node]['value']-G.node[x]['value']) if G.node[node]['value']>G.node[x]['value'] else 0 for node in G.neighbors(x)})/neighborsHigher

            if neighborsPlainHigher == 0:
                G.node[x]['newPlainValue'] = G.node[x]['plainValue']
            else:
                G.node[x]['newPlainValue'] = G.node[x]['plainValue'] + C*sum({(G.node[node]['plainValue']-G.node[x]['plainValue']) if G.node[node]['plainValue']>G.node[x]['plainValue'] else 0 for node in G.neighbors(x)})/neighborsPlainHigher
                
                # G.node[x]['newValue'] = G.node[x]['value'] + C*sum({G.node[node]['value']-G.node[x]['value'] for node in G.neighbors(x)})/len(G.neighbors(x)) 

        count += 1
        vsum = 0
        pvsum = 0

        for x in G.nodes():
            G.node[x]['value'] = G.node[x]['newValue']
            G.node[x]['plainValue'] = G.node[x]['newPlainValue']
            
            vsum += G.node[x]['value']
            pvsum += G.node[x]['plainValue']
            
        ccdfx.append(count)
        ccdfy1.append(vsum/G.number_of_nodes())
        ccdfy2.append(pvsum/G.number_of_nodes())

    return (ccdfx,ccdfy1,ccdfy2)

ret1 = compute(0.01,"data/nw_gen_10000_3_0_1_2.graphml")

plt.plot(ret1[0],ret1[1],'r',marker='o')
plt.plot(ret1[0],ret1[2],'g',marker='o')

plt.title("nth step - average")
plt.ylabel("average")
plt.xlabel("nth step")

# draw graph in inset
plt.axes([0.45,0.45,0.45,0.45])
# Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
# pos=nx.spring_layout(Gcc)
plt.axis('off')
# nx.draw_networkx_nodes(Gcc,pos,node_size=20)
# nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

plt.savefig("nth step - average.png")
plt.show()

#"data/nw_gen_10000_1.graphml"