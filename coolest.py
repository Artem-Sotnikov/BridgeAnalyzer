#!./bin/python3
from anastruct import SystemElements as SE
import math
import pandas as pd
import yaml
import matplotlib.pyplot as plt
CONFIG_PATH = 'config.yaml'

def validate_config(config: dict) -> list: 
    '''
    Validates the configuration file based in its internal parameters
    
    Parameters
    ----------
    config: dict 
        The contents of the yaml config files

    Returns
    -------
    list:
        The error log of the problems with the configuration file
    '''

    # Check for pin/roller supports
    config_error_log = [] #relevant errors to be logged

    if config['constraints']['enforce_support_level']:
        x_level = config['pin_supports'][0]['x']
        for support in config['roller_supports'] + config['pin_supports']:
            if support['x'] != x_level:
                config_error_log.append('Supports are not at the same level')
                break

    if (not config['pin_supports']):
        config_error_log.append("No pin supports")
    if (not config['roller_supports']):
        config_error_log.append("No roller supports")
    if (not config['point_loads']):
        config_error_log.append("No point loads")

    return config_error_log

def validate_truss(config, truss) -> list: 
    #TODO finish the function; not done yet
    '''
    Validates the truss structure based on the constraints of the config file
    
    Parameters
    ----------
    config: dict 
        The contents of the yaml config files
    truss: anastruct.SystemElements
        The truss object

    Returns
    -------
    list:
        The error log of the problems with the configuration file
    '''
    # Check for pin/roller supports
    config_error_log = [] #relevant errors to be logged

    if config['constraints']['enforce_support_level']:
        x_level = config['pin_supports'][0]['x']
        for support in config['roller_supports'] + config['pin_supports']:
            if support['x'] != x_level:
                config_error_log.append('Supports are not at the same level')
                break
    
    if (not config['pin_supports']):
        config_error_log.append("No pin supports")
    if (not config['roller_supports']):
        config_error_log.append("No roller supports")
    if (not config['point_loads']):
        config_error_log.append("No point loads")

    return config_error_log

# make sure lengths are in mm and thus the forces are in N
# return minimum second moment of area
def euler_buckling_load(config: dict, force: float, length: float) -> float:
    secondMomentOfArea = (abs(force) * length ** 2) / (math.pi ** 2 * config['material_properties']['member']['E'])
    return secondMomentOfArea

def find_crossectional_area(config: dict, axial_load: float) -> float:
    return axial_load/config['material_properties']['member']['tensile_ultimate']

if __name__ == '__main__':
    # Load the yaml file
    with open(CONFIG_PATH) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    # Validate yaml file
    error_log = validate_config(config)
    if not error_log:
        raise Exception('You are bad')

    # Create the SystemElements object
    truss = pd.read_csv(config['data_path'])
    ss = SE()
    for i in zip(truss['Start X'], truss['Start Y'], truss['End X'], truss['End Y'], truss['Length']):
        ss.add_truss_element([[i[0], i[1]], [i[2], i[3]]])

    # Adding pin supports
    for i in config['pin_supports']:
        try:
            ss.add_support_hinged(ss.find_node_id([i['x'], i['y']]))
        except AttributeError as e:
            print('pin support node not found: ', i['x'], i['y'])

    # Adding roller supports
    for i in config['roller_supports']:
        try: 
            ss.add_support_roll(ss.find_node_id([i['x'], i['y']]))
        except AttributeError as e:
            print('roller support node not found: ', i['x'], i['y'])

    # Adding point loads
    for i in config['point_loads']:
        try:
            node_id = ss.find_node_id(vertex=[i['location']['x'], i['location']['y']])
            ss.point_load(node_id, Fy=i['magnitude'])
        except AttributeError as e:
            print('point load node not found: ', i['location']['x'], i['location']['y'])

    ss.solve()
    results = ss.get_element_results()
    forceList = [i['N'] for i in results]
    max_force, min_force = {'N': -math.inf}, {'N': math.inf}
    bridge_weight = 0 # this can't be determined rn :(

    for i in results:
        print('%i) axial load: %.3f' % (i['id'], i['N']), end=' ')
        if i['N'] > max_force['N']:
            max_force = i
        if i['N'] < min_force['N']:
            min_force = i 
        if i['N'] > 0: # tension
            A = find_crossectional_area(config, i['N'])
            print('min crossectional area: %.3f' % A)
            bridge_weight += A*i['length']*config['material_properties']['member']['density']
        else: # compression
            I = euler_buckling_load(config, i['N'], i['length'])
            print('min 2nd moment of area: %.3f' % I)
            # bridge_weight += 12*i['length']*I/\
            #     config['design_parameters']['thickness_increment']**2 *\
            #     config['material_properties']['member']['density']
            bridge_weight += 12**(1/3)*i['length']*I**(1/3)*\
                config['design_parameters']['thickness_increment']**(2/3)*\
                config['material_properties']['member']['density']
        print()

    bridge_weight += bridge_weight + len(ss.node_map)*config['constraints']['bridge_width']*config['material_properties']['pin']['density']

    pvRatio = -config['point_loads'][0]['magnitude']/9.81*1000/bridge_weight * 2
    print("Max force %.3f N at node %i" % (max_force['N'], max_force['id']))
    print("Min force %.3f N at node %i" % (min_force['N'], min_force['id']))
    print("Bridge Weight: %.5f g" % (bridge_weight))
    print("PV Ratio: %.3f" % (pvRatio))
    plt.hist(forceList)
    plt.show()

    # TODO: Check if members break/consider material properties
    ss.show_structure()
