"""
node for search tree, includes state, pointer to parent node,
steps or actions, depth and path cost
"""
class Node(object):
    def __init__(self, state, parent, step=None, depth=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.step = step  
        self.depth = depth
        self.path_cost = path_cost

    @property
    def display_states(self):
            return ''.join([str(i) for row in self.state for i in row]) + str(self.step if self.step is not None else -1)
        
  #creating a fringe 
class Fringe(object):
    def __init__(self):
        self.items = []
      #cheking if the fringe is empty  
    def is_empty(self):
        return len(self.items) == 0

    def create_fringe(self, item):
        self.items = item   

    def add_fringe(self, item):
        self.items.insert(0, item)
   #pop operation remove item
    def pop_item(self):
        return self.items.pop(0)

    def extend_fringe(self, item):
        self.items.extend(item)



class Search(object):
    def __init__(self, initial_state, expand_node, goal_test):
        self.goal_test = goal_test
        #root node initiation, parent none, step none, depth 1 path cost 1
        self.nodes = [Node(initial_state, None, None, 1, 1)]  
        
        self.display_stateses = {self.nodes[0].display_states: self.nodes[0]}
        self.expand_node = expand_node
        #initiate fringe 
        self.fringe = Fringe()
        self.fringe.create_fringe(self.expand_node(self.nodes[0]))

  #create a function  list all the steps taken for solution
    @staticmethod
    def path_to_solution(node):
        list_of_steps = []

        while node.parent is not None:
            list_of_steps.append(node.step)
            node = node.parent
        #reverse the step list to see from starting to end 
        list_of_steps = list_of_steps[::-1]  

        return list_of_steps

    def search_path(self, steps=None, search_cost=0):
        count = 1
         
        #continue as long as fringe has element
        while not self.fringe.is_empty():
            node = self.fringe.pop_item()
            print ("Depth = ", node.depth)
            print ("New state ",  node.display_states)
            print()
            

            if self.goal_test(node):
                return self.path_to_solution(node), node
            expanded_nodes = [a_node for a_node in self.expand_node(node) if a_node.display_states not in self.display_stateses]

            for a_node in expanded_nodes:
                a_node.path_cost += search_cost
                self.display_stateses[a_node.display_states] = a_node
           
            self.fringing(expanded_nodes)

            count += 1

        return False, None

class Depth_Lim_Search(Search):
    def __init__(self, initial_state, expand_node, goal_test, depth_limit):
        Search.__init__(self, initial_state, expand_node, goal_test)
        self.depth_limit = depth_limit
    def fringing(self, nodes):
        nodes = [node for node in nodes if node.depth <= self.depth_limit]
        self.fringe.items = nodes + self.fringe.items
   

