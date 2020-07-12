
#This is a test :P
import anastruct

#Add all elements to truss
def createMembers(vertexList, ss):
    #each element contains two vertex objects, use to construct truss elements
    for element in vertexList:
        ss.add_truss_element(location=[element[0],element[1]])

#Add pin and roller support to appropriate nodes
#Based on left support being at 0,0 and right support being at 14,0
def addSupports(ss):
    for key,val in ss.node_map:
        #leftmost support is a roller support
        if val.x == 0 and val.y == 0:
            ss.add_support_roll(key, direction=='y')
        #rightmost support is a hinged support
        elif val.x == 14 and val.y == 0:
            ss.add_support_hinged(key)

#Add distributed loads to nodes directly supporting the train
def addLoads(ss):
    totalLoad = 28 #Total distributed load for 2D truss
    nodeCount = 0 #Number of nodes that load is being distributed on

    loadNodes = []

    #Iterate through all nodes and keep track of which nodes have point loads
    #Also keep track of how many nodes to distribute load on
    for key,val in ss.node_map:
        if val.x == 0:
            nodeCount = nodeCount + 1
            loadNoads.append(key)

    distributedLoad = totalLoad / nodeCount #point load on each node

    #Add load to relevant points
    for node in loadNodes:
        ss.point_load(node, Fy=-distributedLoad)

#not really sure if this works
def runSimulation(ss):
    ss.solve()
    ss.show_structure()
    ss.show_reaction_force()
    ss.show_axial_force()
