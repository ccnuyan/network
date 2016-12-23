'''
moudle main
'''

from experiment import Experiment as Experiment

RADIUS = None
OMEGA = 0.1
LOOPS = 300
RANDOM_LINKS = 1

PARAMS = {
    'cfd_radius': RADIUS,
    'random_links': RANDOM_LINKS,
    'omega': OMEGA,
    'sph':0.8,
    'h_1':0.9,
    'h_2':0.6,
}

EXP = Experiment(
    'data/uniform_100in100informed.graphml', params=PARAMS, )

# EXP.link_randomly()

while LOOPS > 0:
    EXP.load()

    EXP.clear_links()
    EXP.link_randomly()

    # EXP.link_all_in_radius()
    # EXP.update_pl()
    EXP.update_ll()
    print(LOOPS)
    LOOPS -= 1

EXP.draw_thita(show=False, number=1)
EXP.draw_thita(show=False, number=2)
# EXP.show_degree_sequence(show=False)
# EXP.finalize()
