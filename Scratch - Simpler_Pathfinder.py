
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


def check_path(grid, candidates, current_node, parent, destination):
    cx, cy = current_node.x, current_node.y
    if current_node == destination:
        return [destination]
    
    valid_nbrs = {nbr for nbr in [grid[ny][nx] for (ny,nx) in get_nbrs(cy,cx)] 
                    if type(nbr) is Node and nbr in candidates} - {parent}
    print(f'Cnode {current_node}, Nb: {valid_nbrs}')
    if not valid_nbrs:
        candidates.remove(current_node)
        return None
    else:
        paths = []
        for nbr in valid_nbrs:				
            current_path = check_path(grid, candidates, nbr, current_node, destination)		#Recursion
            if current_path:
                    if destination in current_path:
                        paths.append(current_path)    
            best_path = min(paths, default=[], key=lambda x: len(x) if len(x)>0 else None)
            candidates.remove(current_node)
        return [] if not best_path else best_path.append(current_node)


grid = [['.' for p in range(6)] for r in range(6)]
nodes = [(0,0), (0,1), (0,2), (1,1), (1,2), (2,2), (3,2), (3,3), (2,4), (3,4), (4,4)]
nids = IT.count(0)
for node in nodes:
    nx, ny = node
    grid[ny][nx] = Node(nx, ny, next(nids))
candidates = [spot for spot in [grid[ny][nx] for nx in range(6) for ny in range(6)] if type(spot) is Node]
print(candidates)
from pprint import pprint
pprint(grid)

best_path = check_path(grid, candidates, grid[0][0], '_noparent', grid[4][4])
print(best_path)

