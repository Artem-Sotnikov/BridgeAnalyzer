'''
Created on Jul 12, 2020

@author: Artem Sotnikov
'''

import coolCalculator
import anastruct
from data_extractor import DataExtractor

if __name__ == "__main__":
    print('Bridge Analyser active!')
    
    extractor = DataExtractor() 
    output_list = extractor.extract_data("test_data_extract3.csv")    

    ss = anastruct.SystemElements()
    
    nodeDict, bridgeCost = coolCalculator.createMembers(output_list, ss)

    print(nodeDict)
    
    coolCalculator.addSupports(ss, nodeDict)
    coolCalculator.addLoads(ss, nodeDict)
    coolCalculator.runSimulation(ss)
