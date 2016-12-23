from experiment import Experiment as Experiment

#### for link_s:
# None means 'None'
# 0 means 'All'
# negative value means nearst agents
# positive value means random values in radius

#### for link_d:
# None means 'None'
# 0 means 'None'
# negative value means random agents
# positive value means agents obey cdf

todos = [[1, None, 0.5, 0.1]]


# todos = [[None, 1, 1, 0.1], [None, 1, 0.5, 0.1], [None, 1, 0.05, 0.1]]
# todos = [[1, 1, 1, 0.1], [1, 1, 0.5, 0.1], [1, 1, 0.05, 0.1]]
# todos = [[1, 0, 1, 0.1], [1, 0, 0.5, 0.1], [1, 0, 0.05, 0.1]]
# todos = [[5, 0, 0.5, 0.1], [5, 1, 0.5, 0.1]]

# todos = [[1, 0, 0.05, 0.1], [None, 1, 0.05, 0.1]]
# todos = [[1, 0, 0.2, 0.1], [None, 1, 0.2, 0.1]]

# todos = [[1, 1, 0.5, 0.01], [2, 1, 0.5, 0.01], [5, 1, 0.5, 0.01]]
# todos = [[-1, 0, 0.5, 0.01], [-2, 0, 0.5, 0.01]]

# todos = [[None, 1, 0.5, 0.1], [None, 2, 0.5, 0.1], [None, 5, 0.5, 0.1]]

# compare of bias radius with symmetric radius
# todos = [[1, 1, 0.5, 0.1}], [2, 1, 0.5, 0.1}]]
# todos = [[1, 1, 0.5, {'bias':0.8, 'ep': 0.1}], [2, 1, 0.5, {'bias':0.8, 'ep': 0.1}]]

# todos = [[None, 1, 0.5, 0.01], [None, -1, 0.5, 0.3], [0, 0, 0.5, 0.3]]

for todo in todos:
    link_s = todo[0]
    link_d = todo[1]
    omega = todo[2]
    cfd_radius = todo[3]

    # experiment = Experiment('data/uniform_20in1000informed.graphml', cfd_radius=cfd_radius, link_s=link_s, link_d=link_d, omega=omega)
    # experiment.link()
    # experiment.show_degree_sequence(show=False)

    count = 3000

    experiment = Experiment('data/uniform_20in100informed.graphml', cfd_radius=cfd_radius, link_s=link_s, link_d=link_d, omega=omega)

    # while count > 0 and experiment.get_avg_distance() > 0.001:
    while count > 0:
        experiment.link()
        experiment.update()
        print(count)
        count -= 1

    experiment.draw_thita1(show=False)
    # experiment.draw_thita2(show=False)
    # experiment.show_degree_sequence(show=False)



