#This is a test :P
#Maximo's kickass code
import anastruct

#Add all elements to truss
def createMembers(vertexList, ss):
    #each element contains two vertex objects, use to construct truss elements

    outputList = {} #dictionary where key is nodeID and val are coordinates
    nodeCount = 1 #nodeID of current node being added

    bridgeCost = 0.0
    
    for element in vertexList:
        ss.add_truss_element(location=[element[0],element[1]])

        bridgeCost += element[2] * 10;

        if element[0] not in outputList.values():
            outputList[nodeCount] = element[0]
            nodeCount = nodeCount + 1
            
        if element[1] not in outputList.values():
            outputList[nodeCount] = element[1]
            nodeCount = nodeCount + 1

    bridgeCost += 5 * (nodeCount - 1)
    
    return outputList, bridgeCost

#Add pin and roller support to appropriate nodes
#Based on left support being at 0,0 and right support being at 14,0
def addSupports(ss, outputList):
    for key, val in outputList.items():
        #leftmost support is a roller support
        if val[0] == 0 and val[1] == 0:
            ss.add_support_roll(key, direction=2)
        #rightmost support is a hinged support
        elif val[0] == 14 and val[1] == 0:
            ss.add_support_hinged(key)

#Add distributed loads to nodes directly supporting the train
def addLoads(ss, outputList):
    totalLoad = 28.0 #Total distributed load for 2D truss
    nodeCount = 0 #Number of nodes that load is being distributed on

    loadNodes = {}

    #Iterate through all nodes and keep track of which nodes have point loads
    #Also keep track of how many nodes to distribute load on
    for key,val in outputList.items():
        if int(float(val[1])) == 0:
            nodeCount = nodeCount + 1
            loadNodes[key] = val

    distributedLoad = totalLoad / float(nodeCount) * 1000 #point load on each node

    #Add load to relevant points
    for key in loadNodes.keys():
        ss.point_load(key, Fy=-distributedLoad)

#not really sure if this works
def runSimulation(ss):
    ss.show_structure()
    ss.show_reaction_force()
    ss.show_axial_force()

#Returns list of dictionary for each member (force, length)
def returnForceDict(ss):
    outputList = []
    for element in ss.get_element_results():
        outputList.append({'id' : element['id'], 'length' : element['length'], 'force' : element['N']})

    return outputList
        


#Check if it is possible to construct bridge with doubled up members
#Return True if bridge is valid, false if not
def isValidForces(outputList):
    
    for element in outputList:
        if element['force'] < -16000 or element['force'] > 20000:
            return False
        
    return True

#Update cost to account for doubled up members
def updateCost(outputList, bridgeCost):

    doubledMemberList = []
    
    for element in outputList:
        #check if force is high enough to warrant doubleing up, but not too high to be invalid
        if (element['force'] < -8000 and element['force'] > - 16000) or element['force'] > 10000 and element['force'] < 20000:
            bridgeCost += element['length']*10
            doubledMemberList.append(element['id'])    

    print(doubledMemberList)
    return bridgeCost

