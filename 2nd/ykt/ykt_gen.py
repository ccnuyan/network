import json
import networkx as nx

file = 'data.json'

with open(file) as json_data:
    d = json.load(json_data)

    G = nx.Graph()

    for node in d:
        G.add_node(node['Source'])
        G.add_node(node['Target'])
        G.add_edge(node['Source'], node['Target'])
if not nx.is_connected(G):
    component = 0
    max = 0
    for cp in nx.connected_component_subgraphs(G):
        if len(cp.nodes()) > max:
            max = len(cp.nodes())
            component = cp
    G = component
nx.write_graphml(G,'data.graphml')
        