#This is a test :P
#Maximo's (and Artem's) kickass code
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
    load = 2000.0
    nodeCount = 0 #Number of nodes that load is being distributed on
    nodeDist = 999.0 #Shortest distance between nodes on the bottom
    referenceNode = 0.0
    
    loadNodes = {}

    print("Output LIST: ")
    print(outputList)

    #Iterate through all nodes and keep track of which nodes have point loads
    #Also keep track of how many nodes to distribute load on
    for key,val in outputList.items():
        if int(float(val[1]) == 0):
            nodeCount = nodeCount + 1
            loadNodes[key] = val
            if nodeCount == 1:
                referenceNode = float(val[0])
            elif nodeCount > 1:
                nodeDist = min(abs(nodeDist), abs(referenceNode - float(val[0])))

    print ("NODE DIST" + str(nodeDist))
    print ("Nodelist")
    print(loadNodes)

    #Add load to relevant points
    for key,val in loadNodes.items():
        if float(val[0]) == 0 or float(val[0]) == 14:
            ss.point_load(key, Fy=-load*nodeDist*0.5)
        elif float(val[1] == 0):
            ss.point_load(key, Fy=-load*nodeDist)

    print("nodeDist: " + str(nodeDist))
    
    if nodeCount < 5:
        print("Not enough nodes along base, calculations aborted")
        return False

    return True

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

def isSimpleTruss(number_of_nodes, number_of_elements):
    return (number_of_elements == 2*(number_of_nodes) - 3)

#Check if it is possible to construct bridge with doubled up members
#Return True if bridge is valid, false if not
def isValid(outputList):
    returnVal = True
    
    for element in outputList:
        if element['force'] < -16000 or element['force'] > 20000:
            print("One of your forces exceeds the max: " + str(element['id']) + ": " + str(element['force']))
            returnVal = False
        if element['length'] < 1:
            print ("One of your members is too short: " + str(element['id']) + ": " + str(element['length']))
            returnVal = False
        
    return returnVal

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



