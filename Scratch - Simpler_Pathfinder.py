
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


def find_short_path(grid, current_node, parent_path, destination):
    ''' Walks through node network to identify: valid paths from A to B.  Does not require that all nodes be visited
    '''
    cx, cy = current_node.x, current_node.y
    if current_node in parent_path:
        return False    #Loop
    this_path = list(parent_path)
    this_path.append(current_node)
    #print(this_path)
    if current_node == destination:
        valid_paths.append(this_path)
        print(valid_paths)
        return True
    valid_nbrs = {nbr for nbr in [grid[ny][nx] for (ny,nx) in get_nbrs(cy,cx)] if type(nbr) is Node} - set(this_path)
    #print(f'Cnode {current_node}, Nb: {valid_nbrs}')
    if not valid_nbrs:
        return False    # Dead End
    for nbr in valid_nbrs:				
        find_short_path(grid, nbr, tuple(this_path), destination)    #Recursion
    return None

def follow_a_path(self, grid, destination):
    ''' Robot method to follow a chalk line path; 
        Prefers to go forward before looking to turn'''
    not_visited = grid.nodes[:]
    visited = []
    trail = []
    self.pos = (self.x, self.y)
    self.hdg

    while not_visited and self.pos not destination:
        if self.pos + self.hdg == valid_node:
            visted.append(not_visited.remove(current_node))
            trail.append('fwd')
            self.move_fwd() 
        else:
            self.turn_left()

    
    

def get_image(stream):
    ''' Reads a text stream,
    and stores data for each new Pixel object
    Returns an array (tuple of tuples) of Pixel objects'''
    screen = stream.rstrip('\n\r').splitlines()
    pixels = [[Point(jcol,irow,p) 
           for jcol,p in enumerate(row)] 
           for irow,row in enumerate(screen)]
    #logging.debug(pixels[:][:])
    return tuple((tuple(line) for line in pixels))

test_grid ='''........
.XXXXXX.
.X....X.
.XXXXXX.
.X..X.X.
..XXX.X.
....XXX.
........'''

#grid = [['.' for p in range(6)] for r in range(6)]
#nodes = [(1,1), (1,2), (1,3), (1,4), (2,3), (3,3), (3,4), (4,4), ()]

grid = get_image(test_grid)
from pprint import pprint
#pprint(grid)
nids = IT.count(0)
nodes = [[Node(p.x, p.y, next(nids)) if p.state == 'X' else p for p in row ] for row in grid]
#pprint(nodes)

valid_paths = []
find_short_path(nodes, nodes[1][1], tuple(), nodes[6][6])
 
best_path = min(valid_paths, key=len, default='No valid paths')
pprint(f'Best Path is: {best_path}')
pprint([n.node_id for n in best_path])
pprint([[n.node_id for n in path] for path in valid_paths])

