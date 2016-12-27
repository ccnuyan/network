from experiment import Experiment as Experiment

cfd_radius = 0.1
omega = 0.1
count = 1000

experiment = Experiment('data/uniform_20in100informed.graphml', cfd_radius=cfd_radius, omega=omega)

while count > 0:
    experiment.link()
    experiment.show_degree_sequence(show=False)
    experiment.update()
    print(count)
    count -= 1

experiment.draw_thita1(show=False)
experiment.draw_thita2(show=False)
experiment.show_degree_sequence(show=False)
experiment.finalize()
