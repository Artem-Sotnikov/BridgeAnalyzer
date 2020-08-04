'''
Created on Jul 12, 2020

@author: Artem Sotnikov (and Maximo van der Raadt :O)
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
