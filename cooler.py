#!/use/bin/env python3
from anastruct import SystemElements as SE
import pandas as pd

if __name__ == '__main__':
    file = pd.read_csv('truss.csv')
    ss = SE()
    cost = 0
    for i in file.itertuples():
        end_points = [[i[4], i[5]], [i[7], i[8]]]
        ss.add_truss_element(end_points)
        cost += i.Length * 10
        if end_points[0][1] == 0 and end_points[1][1] == 0:
            ss.q_load(-2, ss.id_last_element)

    ss.add_support_hinged(ss.find_node_id([0,0]))
    ss.add_support_roll(ss.find_node_id([14,0]))

    ss.solve()
    ss.show_structure()
    # ss.show_reaction_force()
    ss.show_axial_force()
    results = ss.get_element_results()

    cost += len(ss.node_map) * 5

    print('there were a total of %d plates and %d members' % (len(ss.node_map), len(ss.element_map)))
    print('simple truss index: %d' % (len(ss.node_map)*2-3-len(ss.element_map)))
    print('total cost brings you $%f' % cost)

    print([(i['id'], i['N']) for i in results])
    