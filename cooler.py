#!./bin/python3
from anastruct import SystemElements as SE
import pandas as pd

if __name__ == '__main__':
    truss = pd.read_csv('truss.csv')
    ss = SE()
    cost = 0
    for i in zip(truss['Start X'], truss['Start Y'], truss['End X'], truss['End Y'], truss['Length']):
        ss.add_truss_element([[i[0], i[1]], [i[2], i[3]]])
        cost += i[4] * 10
        if i[1] == 0 and i[3] == 0:
            ss.q_load(-2, ss.id_last_element)

    ss.add_support_hinged(ss.find_node_id([0,0]))
    ss.add_support_roll(ss.find_node_id([14,0]))

    ss.solve()
    results = ss.get_element_results()
    print([(i['id'], i['N']) for i in results])

    cost += len(ss.node_map) * 5

    print('there were a total of %d plates and %d members' % (len(ss.node_map), len(ss.element_map)))
    print('simple truss index: %d (0 means simple truss)' % (len(ss.node_map)*2-3-len(ss.element_map)))
    for i in results:
        if i['N'] > 10 or i['N'] < -8:
            cost += i['length'] * 10
    print('total cost brings you $%f' % cost)

    ss.show_axial_force()
    ss.show_structure()
    ss.show_reaction_force()
