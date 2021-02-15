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
def euler_buckling_load(config, force, length):
    '''
    Calculates the euler buckling load.
    
    Parameters
    ----------
    config: dict 
        The contents of the yaml config files
    force: float
        The force being exerted as compression in this member (in N)
    length:
        The length of the member

    Returns
    -------
    float:
        The second moment of area that this member will need to achieve in order to not break
    '''
    secondMomentOfArea = (force * pow(length, 2)) / (pow(math.pi,2) * config.member.E)
    return secondMomentOfArea

def find_crossectional_area(member_loads: dict):
    '''
    Calculates the cross-sectional area of all members.
    
    Parameters
    ----------
    config: dict 
         containing the loads (in N) on all the members
    
    Returns
    -------
    
    '''
    for i in member_loads:
        pass

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
    print(results)
    forceList = []
    max_force = -999999 
    min_force = 999999

    for i in results:
        print((i['id'], i['N']))
        forceList.append(i['N'])
        if i['N'] > max_force:
            max_force = i['N']
        if i['N'] < min_force:
            min_force = i['N']

    print("Max force ", max_force)
    print("Min force ", min_force)
    plt.hist(forceList)

    # TODO: Check if members break/consider material properties
    ss.show_structure()
