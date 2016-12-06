from experiment import Experiment as Experiment

todos = [[0, 1, 0.5, 0.1], [0, 2, 0.5, 0.1], [0, 5, 0.5, 0.1], [0, 10, 0.5, 0.1]]
# todos = [[0, 1, 1, 0.1], [0, 1, 0.5, 0.1], [0, 1, 0.05, 0.1]]
# todos = [[1, 1, 1, 0.1], [1, 1, 0.5, 0.1], [1, 1, 0.05, 0.1]]
# todos = [[1, 0, 1, 0.1], [1, 0, 0.5, 0.1], [1, 0, 0.05, 0.1]]
# todos = [[5, 0, 0.5, 0.1], [5, 1, 0.5, 0.1]]


for todo in todos:
    link_s = todo[0]
    link_d = todo[1]
    omega = todo[2]
    cfd_radius = todo[3]

    count = 100

    experiment = Experiment('data/uniform_20in100informed.graphml', cfd_radius=cfd_radius, link_s=link_s, link_d=link_d, omega=omega)

    while count > 0:
        experiment.link()
        experiment.update()
        print(count)
        count -= 1

    experiment.draw_thita1(show=False)
    experiment.draw_thita2(show=False)
    experiment.show_degree_sequence(show=False)
