'''
Created on Jul 12, 2020

@author: Artem Sotnikov
'''

from cool_calculator import CoolCalculator
import anastruct
from data_extractor import DataExtractor

if __name__ == "__main__":
    print('Bridge Analyser active!')
    
    extractor = DataExtractor() 
    #output_list = extractor.extract_data("test_data_extract3.csv")
    input_list = extractor.extract_data("bridge3v5.csv")  
    manual_list = [ [(0.0,0.0), (7.0,0.0), 7.0] , [(7.0,0.0), (14.0,0.0), 7.0] ]

    cool_calculator = CoolCalculator(input_list)
    cool_calculator.set_debug_mode(True)
    cool_calculator.set_ignore_design_rules(True)
    
    cool_calculator.run_analysis()
    cool_calculator.display_simulation_results()
#     print(cool_calculator.bridge_cost)
    
#     nodeDict, bridgeCost = cool_calculator.create_members_from_list(output_list, ss)
# 
#     #print(nodeDict)
#     
#     cool_calculator.add_supports(ss, nodeDict)
# 
#     if not cool_calculator.add_loads(ss, nodeDict):
#         exit()
#     if not cool_calculator.isSimpleTruss(len(nodeDict), len(output_list)):
#         print('Bridge is not a simple truss, calculations aborted')
#         exit()
#     
#     ss.solve()
#     
#     forceDict = cool_calculator.construct_force_dict(ss)
#      
#     if cool_calculator.check_forces(forceDict):
#         print("Very valid, much wow")
#         bridgeCost = cool_calculator.updateCost(forceDict, bridgeCost)
#         print("Cost: $" + str(bridgeCost))
#     else:
#         print("Not valid, very sad :(")
#         print("Cost: Your bridge is bad and so are you")    
# 
#     cool_calculator.display_simulation_results(ss)
#     
#     print(forceDict)
 
