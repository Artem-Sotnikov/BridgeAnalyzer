#This is a test :P
#Maximo's (and Artem's) kickass code
import anastruct

class CoolCalculator:
    def __init__(self, bridge_data):
        
        self.debug_mode = False;
        
        self.ss = anastruct.SystemElements()
        self.bridge_cost = 0.0
        self.raw_element_list = bridge_data
        
        self.node_dict = {} #dictionary where key is nodeID and val are coordinates
        
        # Bridge design rule fields
        self.is_simple_truss = False
        self.has_valid_load_distribution = False
        self.has_valid_members = False
         
        self.results_dict_list = [] #list of dictionaries in the form {id, length, force} for every member after calculation
        
        self.is_valid = False
    
    def set_debug_mode(self, debug):
        self.debug_mode = debug
    
    # All-encompassing function that will perform a basic check
    def run_analysis(self):
        vertex_list = self.raw_element_list
        
        self.create_members_from_list(vertex_list)
        
        if (self.debug_mode):
            print(self.bridge_cost)
        
        self.add_supports()
        self.add_loads()
        
        if (not (self.has_valid_load_distribution and self.is_simple_truss and self.has_valid_members )):
            print('Design check was aborted before calculation.\n' + \
                    'You should feel bad; your bridge does not even qualify based on the design rules alone.\n' +\
                    'The status report can be reviewed below: \n')
            print('Bridge is a simple truss: ' + str(self.is_simple_truss));
            print('Bridge has a valid load distribution: ' + str(self.has_valid_load_distribution))
            print('Bridge has all members > 1m: ' + str(self.has_valid_members))
            return
        
        self.ss.solve()   
        self.construct_force_dict()
        self.check_forces()
        self.update_cost()
        
        if (self.is_valid):
            print('The bridge design was fully valid :)')
            print('Bridge cost: $' + str(self.bridge_cost))
        else:
            print('Your bridge design is bad and you are bad. The forces don\'t check out :(')
        
            
    #Add all elements to truss
    def create_members_from_list(self, vertex_list):
    
        node_count = 1 #nodeID of current node being added, ids start with 1 :(
        self.has_valid_members = True #preliminarily set to true, if any fail the test will be set to false
        
        #each element contains two vertex objects, use to construct truss elements
        for element in vertex_list:
            self.ss.add_truss_element(location=[element[0],element[1]])
    
            self.bridge_cost += element[2] * 10;
            
            if (element[2] < 1):
                self.has_valid_members = False
    
            if element[0] not in self.node_dict.values():
                self.node_dict[node_count] = element[0]
                node_count = node_count + 1
                
            if element[1] not in self.node_dict.values():
                self.node_dict[node_count] = element[1]
                node_count = node_count + 1
        
        true_node_count = node_count - 1
        self.bridge_cost += 5 * (true_node_count)
        
        if (not self.check_simple_truss(true_node_count, len(vertex_list))):
            self.is_simple_truss = False
        else:
            self.is_simple_truss = True
        
    
    #Add pin and roller support to appropriate nodes
    #Based on left support being at 0,0 and right support being at 14,0
    def add_supports(self):
        for key, val in self.node_dict.items():
            #leftmost support is a roller support
            if val[0] == 0 and val[1] == 0:
                self.ss.add_support_roll(key, direction=2)
            #rightmost support is a hinged support
            elif val[0] == 14 and val[1] == 0:
                self.ss.add_support_hinged(key)
    
    #Add distributed loads to nodes directly supporting the train
    def add_loads(self):
        totalLoad = 28.0 #Total distributed load for 2D truss
        nodeCount = 0 #Number of nodes that load is being distributed on
    
        loadNodes = {}
    
        #Iterate through all nodes and keep track of which nodes have point loads
        #Also keep track of how many nodes to distribute load on
        for key,val in self.node_dict.items():
            if int(float(val[1])) == 0:
                nodeCount = nodeCount + 1
                loadNodes[key] = val
                
        if nodeCount < 5:
            self.has_valid_load_distribution = False
            return
        else:
            self.has_valid_load_distribution = True
        
        distributedLoad = totalLoad / float(nodeCount) * 1000 #point load on each node
    
        #Add load to relevant points
        for key in loadNodes.keys():
            self.ss.point_load(key, Fy=-distributedLoad)

    
    #not really sure if this works
    def display_simulation_results(self):
        self.ss.show_structure()
        self.ss.show_reaction_force()
        self.ss.show_axial_force()
    
    # Constructs list of dictionary for each member {id, length, force}
    def construct_force_dict(self):
        for element in self.ss.get_element_results():
            self.results_dict_list.append({'id' : element['id'], 'length' : element['length'], 'force' : element['N']})
    
    
    # Check if the design qualifies as a simple truss   
    @staticmethod
    def check_simple_truss(number_of_nodes, number_of_elements):
        return (number_of_elements == (2*(number_of_nodes) - 3))
    
    #Check if it is possible to construct bridge with doubled up members
    #Return True if bridge is valid, false if not
    def check_forces(self):
        self.is_valid = True
        
        for element in self.results_dict_list:
            if element['force'] < -16000 or element['force'] > 20000:
                self.is_valid = False
                
    
    #Update cost to account for doubled up members
    def update_cost(self):
    
        doubledMemberList = []
        
        for element in self.results_dict_list:
            #check if force is high enough to warrant doubleing up, but not too high to be invalid
            if (element['force'] < -8000 and element['force'] > - 16000) or element['force'] > 10000 and element['force'] < 20000:
                self.bridge_cost += element['length']*10
                doubledMemberList.append(element['id'])    
        
        if self.debug_mode:
            print(doubledMemberList)



