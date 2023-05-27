class Graph: 

    def __init__(self, graph_dict=None):
        self.graph_dict = graph_dict or {}
              

    # add link from A and B of given distance
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance

    # get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # return list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

class Node:

    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # distance to start node
        self.h = 0 # distance to goal node
        self.f = 0 # total cost

    # compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # sort nodes
    def __lt__(self, other):
         return self.f < other.f

    # print node
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))

def astar_search(graph, heuristics, start, end):
    
    # lists for open nodes and closed nodes
    open = []
    closed = []

    start_node = Node(start, None)
    goal_node = Node(end, None)

    #calculate start node travel cost
    start_node.h = heuristics.get(start)
    start_node.f = start_node.g + start_node.h

    # add start node
    open.append(start_node)
    
    # loop until the open list is empty
    while len(open) > 0:

       
        open.sort()                                 # sort open list to get the node with the lowest cost
        current_node = open.pop(0)                  # get node with the lowest cost
        closed.append(current_node)                 # add current node to the closed list
        
        # check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + '-> ' + str(current_node.f))
                current_node = current_node.parent
            path.append(start_node.name + '-> ' + str(start_node.f))
            return path[::-1]

        
        neighbors = graph.get(current_node.name)    # get neighbours
        
        # loop neighbors
        for key, value in neighbors.items():
            neighbor = Node(key, current_node)      # create neighbor node
            if(neighbor in closed):                 # check if the neighbor is in the closed list
                continue

            # calculate full path cost
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h

            # check if neighbor isn't in open list and if it has a lower f value
            # if return true add it to open list
            if(add_to_open(open, neighbor) == True):
                
                open.append(neighbor)

    # return None, no path is found
    return None

# check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True

# create the graph
graph = Graph()
graph.connect('S', 'A', 1)
graph.connect('S', 'G', 12)
graph.connect('A', 'B', 3)
graph.connect('A', 'C', 1)
graph.connect('B', 'D', 3)
graph.connect('C', 'D', 1)
graph.connect('C', 'G', 2)
graph.connect('D', 'G', 3)
# create heuristics
heuristics = {}
heuristics['S'] = 4
heuristics['A'] = 2
heuristics['B'] = 6
heuristics['C'] = 2
heuristics['D'] = 3
heuristics['G'] = 0
# run the algorithm and print the final path
path = astar_search(graph, heuristics, 'S', 'G')
print("Path:", path)
