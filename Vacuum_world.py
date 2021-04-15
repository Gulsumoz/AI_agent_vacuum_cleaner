
import numpy as np
import copy
from DL_search import Depth_Lim_Search


class Vac_World_2X2(object):
    def __init__(self, size=(2, 2), dirt=1):
        self.size = size
        self.dirt = dirt

        # create two 2X2 matrix 
        #matrix 1 Layer 0: dirt, 
        #matrix 2 layer  is vacuum direction (0-up, 1-right, 2-down, 3-left)
        self.world = np.zeros((2, self.size[0], self.size[1]))

        #Dirt Layer set up all the four section have dirt (1 for dirt present,  0 for clean)
        self.world[0].fill(1) 
        #setting up the direction of the vacuum it should be facing toward up direction
        self.world[1].fill(-1)
        self.world[1][1][0] =  0 

    @staticmethod
    def goal_test(node):
        #if all the 4 location is clean goal is achieved
        if np.sum(node.state[0]) == 0:
                return True
        return False


def expand_node(node):
    
    vacuum_x, vacuum_y = np.where(node.state[1] >= 0)
    vacuum_x = vacuum_x[0]
    vacuum_y = vacuum_y[0]
    direction = node.state[1][vacuum_x][vacuum_y]
    expanded_nodes = []
    
    def vacuum_action(state, action):
        cost = 0
        
        if action == 0:
            #sucking up the dirt
            if state[0][vacuum_x][vacuum_y] == 1:
                state[0][vacuum_x][vacuum_y] = 0 
                cost+=1
         #  move forward  
        elif action == 1:
            state = vacuum_move(state)
            cost+=1
        # make turn 
        elif action == 2:
            state[1][vacuum_x][vacuum_y] = (state[1][vacuum_x][vacuum_y] + 1) % 4
            cost+=1
        return state, cost
    
    if node.step == 3:
        return []


    def vacuum_move(state):
      
        if vacuum_stuck(state):
            return state

        if direction == 0:
            state[1][vacuum_x][vacuum_y] = -1
            state[1][vacuum_x - 1][vacuum_y] = direction

        elif direction == 1:
            state[1][vacuum_x][vacuum_y] = -1
            state[1][vacuum_x][vacuum_y + 1] = direction
           
        elif direction == 2:
            state[1][vacuum_x][vacuum_y] = -1
            state[1][vacuum_x + 1][vacuum_y] = direction

        elif direction == 3:
            state[1][vacuum_x][vacuum_y] = -1
            state[1][vacuum_x][vacuum_y - 1] = direction
            #print(direction)

        return state
    
    #if vacuum stuck it should return the state
    def vacuum_stuck(state):
        if (direction == 0 and vacuum_x == 0) or \
                (direction == 3 and vacuum_y == 0) or \
                (direction == 1 and vacuum_y == len(state[0][1]) - 1) or \
                (direction == 2 and vacuum_x == len(state[0][0]) - 1) :
            return True

        return False

    for item in range(4):
        add_node = copy.copy(node)  
        add_node.depth = node.depth + 1
        add_node.parent = node
        add_node.step = item
        new_state, action_cost = vacuum_action(copy.copy(node.state), item)       
        add_node.state = new_state
        add_node.path_cost = node.path_cost + action_cost
        expanded_nodes.append(add_node)
    return expanded_nodes

def main():
    Vac_Environment = Vac_World_2X2((2, 2), 1)
    #do depth limited search with the limit 10
    dls_search = Depth_Lim_Search(Vac_Environment.world, expand_node, Vac_Environment.goal_test, 10)
    print("Initial state of the 2x2 Vacuum Environment;")
    print("First matrix is dirt layer; 1 in each location indicates  dirt")
    print("Second matrix is agent direction, position \n")
    print (Vac_Environment.world)
    print()

    solution, node = dls_search.search_path(search_cost=0)
    numb_of_actions_in_solution= len(solution)+1
    if solution is False:
        print ("No Solution Found\n")

    else:
        print ("Solution found \n")
        print ("Final state of the environment \n" )
        print (node.state, "\n")
        print("Total cost of the solution = ", node.path_cost)
        print ("Solution found at node depth =" , node.depth)
        print("Number of actions in the solution =", numb_of_actions_in_solution)
    
if __name__ == "__main__":
    main()
