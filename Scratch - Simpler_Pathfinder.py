
import itertools as IT

def get_nbrs(row, col):
    '''Returns a tuple of adjacent cell coordinates (Up,Right,Down,Left)
        Assumes (x right, y down)'''  
    #tpadd = lambda a, b: tuple(m+n for m, n in zip(a, b))
    delr = (-1, 0, 1, 0)
    delc = (0, 1, 0, -1)
    nbrs = [tpadd((row, col), z) for z in zip(delr, delc)]
    return tuple(nbrs)  #(up,right,down,left) 

def tpadd(a, b):
    return tuple(m+n for m, n in zip(a, b))


class Point():  
    '''Defines a generic Point data structure to track Location and State information
    Note: state is un-typed for user flexibility.  
    kwargs affords Further flexibility to add attributes to this class'''
    def __init__(self, x, y, state=None, **kwargs):
        self.x = x
        self.y = y
        self.state = state
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, state={self.state})'
        
    #End class Point
    
class Node(Point):
    '''Special type of Point, with linkage to other nodes in a network'''
    def __init__(self, x, y, node_id):
        super().__init__(x, y, state='O', node_id=node_id, nbrs=[], paths=[])

    def __repr__(self):
        return f'Node(id:{self.node_id},x:{self.x}, y:{self.y})'

    #End class Node


def check_path(grid, current_node, parent, destination):
    cx, cy = current_node.x, current_node.y
    if current_node == destination:
        return [destination]
    
    valid_nbrs = set([nbr for nbr in [grid[ny][nx] for (ny,nx) in get_nbrs(cy,cx)] if type(nbr) is Node]) - set(parent)
    print(f'Cnode {current_node}, Nb: {valid_nbrs}')
    if not valid_nbrs:
        return None
    else:
        paths = []
        for nbr in valid_nbrs:				
            current_path = check_path(grid, nbr, current_node, destination)		#Recursion
            if destination in current_path:
                paths.append(current_path)    
            best_path = paths[index(min([len(p) for path in paths]))]
        return [] if not best_path else best_path.append(current_node)


grid = [['.' for p in range(5)] for r in range(5)]
nodes = [(0,0), (0,1), (1,1), (1,2), (2,2), (3,2), (3,3), (3,4), (4,4)]
nids = IT.count(0)
for node in nodes:
	nx, ny = node
	grid[ny][nx] = Node(nx,ny,next(nids))


from pprint import pprint
pprint(grid)


best_path = check_path(grid, grid[0][0], '_noparent', grid[4][4])
print(path)

set(nbr for nbr in if type(nbr) is Node) - set(parent)

