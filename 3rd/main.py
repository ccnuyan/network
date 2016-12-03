from experiment import Experiment as Experiment

cfd_radius = 0.1
omega = 0.05
count = 1000

experiment = Experiment('data/uniform_20in100informed.graphml', cfd_radius=cfd_radius, omega=omega)

while count > 0:
    experiment.link()
    experiment.update()
    count -= 1

experiment.draw_thita1()
experiment.draw_thita2()

# import networkx as nx
# experiment.finalize()
# nx.write_graphml(experiment.G, 'end.graphml')
