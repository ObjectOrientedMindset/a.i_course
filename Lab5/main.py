
# install requirements : pip install pythonds

import sys
from pythonds.basic.stack import Stack
from operator import attrgetter


def display_board(state):
    print( "-------------")
    print( "| %i | %i | %i |" % (state[0], state[3], state[6]))
    print( "-------------")
    print( "| %i | %i | %i |" % (state[1], state[4], state[7]))
    print( "-------------")
    print( "| %i | %i | %i |" % (state[2], state[5], state[8]))
    print( "-------------")


def move_up(state):
    #Moves the blank tile up on the board. Returns a new state as a list.
    new_state = state[:]
    index = new_state.index(0)
    if index not in [0, 3, 6]:
        temp = new_state[index - 1]
        new_state[index - 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None


def move_down(state):
    #Moves the blank tile down on the board. Returns a new state as a list.
    new_state = state[:]
    index = new_state.index(0)
    if index not in [2, 5, 8]:
        temp = new_state[index + 1]
        new_state[index + 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None


def move_left(state):
    #Moves the blank tile left on the board. Returns a new state as a list.
    new_state = state[:]
    index = new_state.index(0)
    if index not in [0, 1, 2]:
        # Swap the values.
        temp = new_state[index - 3]
        new_state[index - 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move it, return None
        return None


def move_right(state):
    #Moves the blank tile right on the board. Returns a new state as a list.
    #Performs an object copy. Python passes by reference.
    new_state = state[:]
    index = new_state.index(0)
    if index not in [6, 7, 8]:
        temp = new_state[index + 3]
        new_state[index + 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None


def create_node(state, parent, operator, depth, cost):
    return Node(state, parent, operator, depth, cost)


def expand_node(node):
    #Returns a list of expanded nodes
    expanded_nodes = []
    expanded_nodes.append(create_node(move_up(node.state), node, "right", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_down(node.state), node, "left", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_left(node.state), node, "down", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_right(node.state), node, "up", node.depth + 1, 0))
    # Filter the list and remove the nodes that are impossible (move function returned None)
    expanded_nodes = [node for node in expanded_nodes if node.state != None]  # list comprehension!
    return expanded_nodes


def bfs(start, goal):
    #Performs a breadth first search from the start state to the goal
    goal=goal
    start_node=create_node(start,None,None,0,0)
    fringe=[]
    fringe.append(start_node)
    current=fringe.pop(0)
    path=[]
    while(current.state!=goal):
        fringe.extend(expand_node(current))
        current=fringe.pop(0)
    while(current.parent!=None):
        path.insert(0,current.operator)
        current=current.parent
    return path
    pass



def greedy(start,goal):
    start_node=create_node(start,None,None,0,0)
    fringe=[]
    path=[]
    fringe.append(start_node)
    current=fringe.pop(0)
    while(current.state!=goal):
        fringe.extend(expand_node(current))
        for item in fringe:
            h(item,goal)
        fringe.sort(key =lambda x: x.heuristic)
        current=fringe.pop(0)
    while(current.parent!=None):
        path.insert(0,current.operator)
        current=current.parent
    return path




def h(state, goal):
    dmatch=0
    for i in range(0,9):
        if state.state[i] != goal[i]:
            dmatch+=1
    state.heuristic=dmatch


#Node data structure
class Node:
    def __init__(self, state, parent, operator, depth, cost):
        #Contains the state of the node
        self.state = state
        #Contains the node that generated this node
        self.parent = parent
        #Contains the operation that generated this node from the parent
        self.operator = operator
        #Contains the depth of this node (parent.depth +1)
        self.depth = depth
        #Contains the path cost of this node from depth 0. Not used for depth/breadth first.
        self.cost = cost

        self.heuristic=None


def readfile(filename, index):
    f = open(filename)
    data = f.read()
    #Get rid of the newlines
    data = data.strip("\n")
    #Break the string into a list using a space as a seperator.
    data = data.split(" ")
    state = []
    for element in data:
        state.append(int(element))
    print(index ,' state: ', state)
    return state



def mainbfs():
    print("bfs :")
    starting_state = readfile(r"state.txt", "initial")
    goal_state = readfile(r"gstate.txt", "final")
    result = bfs(starting_state, goal_state)
    if result == None:
        print( "No solution found")
    elif result == [None]:
        print( "Start node was the goal!")
    else:
        print(result)
        print(len(result), "move")
def maingreedy():
    print("greedy search :")
    starting_state = readfile(r"state.txt", "initial")
    goal_state = readfile(r"gstate.txt", "final")
    result = greedy(starting_state, goal_state)
    if result == None:
        print( "No solution found")
    elif result == [None]:
        print( "Start node was the goal!")
    else:
        print(result)
        print(len(result), "move")

mainbfs()
maingreedy()