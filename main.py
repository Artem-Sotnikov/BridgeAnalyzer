'''
Created on Jul 12, 2020

@author: Artem Sotnikov (and Maximo van der Raadt :O)
'''

import coolCalculator
import anastruct
from data_extractor import DataExtractor

if __name__ == "__main__":
    print('Bridge Analyser active!')
    
    extractor = DataExtractor() 
    #output_list = extractor.extract_data("test_data_extract3.csv")
    output_list = extractor.extract_data("poopybridge.csv")  

    ss = anastruct.SystemElements()
    
    nodeDict, bridgeCost = coolCalculator.createMembers(output_list, ss)

    #print(nodeDict)
    
    coolCalculator.addSupports(ss, nodeDict)

    if not coolCalculator.addLoads(ss, nodeDict):
        exit()
    if not coolCalculator.isSimpleTruss(len(nodeDict), len(output_list)):
        print('Bridge is not a simple truss, calculations aborted')
        exit()
    
    ss.solve()
    
    forceDict = coolCalculator.returnForceDict(ss)
     
    if coolCalculator.isValid(forceDict):
        print("Very valid, much wow")
        bridgeCost = coolCalculator.updateCost(forceDict, bridgeCost)
        print("Cost: $" + str(bridgeCost))
    else:
        print("Not valid, very sad :(")
        print("Cost: Your bridge is bad and so are you")    

    coolCalculator.runSimulation(ss)
    
    print(forceDict)
 
