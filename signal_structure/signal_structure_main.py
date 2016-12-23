'''
moudle main
'''

from signal_structure_experiment import Experiment as Experiment

LOOPS = 1000

PARAMS = {
    'points': 100,
    'density': 0.1,
    'cfd_radius': None,
    'random_links': 2,
    'omega': 0.5,
    'true_state': 0,
    'tp': 0.8,
    'informed': 30,
    'middle': 70,
    'uninformed': 0,
    'p_i_0_0': 0.8,
    'p_i_1_1': 0.8,
    'p_m_0_0': 0.7,
    'p_m_1_1': 0.12,
    'p_u_0_0': 0.4,
    'p_u_1_1': 0.4,
}

EXP = Experiment(params=PARAMS)

# EXP.link_randomly()

EXP.initialize_graph()

while LOOPS > 0:
    EXP.load()
    EXP.update_pl()
    # EXP.update_ll()
    # print(LOOPS)
    LOOPS -= 1

EXP.draw_thita(show=False, number=0)
EXP.draw_thita(show=False, number=1)
EXP.draw_ratio(show=False)
