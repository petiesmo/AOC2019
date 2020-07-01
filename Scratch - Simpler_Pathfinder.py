
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
        test_path.append(current_node)
        valid_paths.append(test_path)
        return True
    valid_nbrs = {nbr for nbr in [grid[ny][nx] for (ny,nx) in get_nbrs(cy,cx)] 
                    if type(nbr) is Node}
    print(f'Cnode {current_node}, Nb: {valid_nbrs}')
    if not valid_nbrs:
        candidates.remove(current_node)
        return False    # Dead End
    test_path.append(current_node)
    for nbr in valid_nbrs:				
        if check_path(grid, nbr, current_node, destination):    #Recursion
            break		
    test_path.remove(current_node)
    candidates.remove(current_node)
    return None

def get_image(stream):
    ''' Runs the input software into the Intcode computer, reads output stream,
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
.X..X...
..XXX...
....XXX.
........'''

#grid = [['.' for p in range(6)] for r in range(6)]
#nodes = [(1,1), (1,2), (1,3), (1,4), (2,3), (3,3), (3,4), (4,4), ()]

grid = get_image(test_grid)
from pprint import pprint
pprint(grid)
nids = IT.count(0)
nodes = [[Node(p.x, p.y, next(nids)) if p.state == 'X' else p for p in row ] for row in grid]
pprint(nodes)
candidates = set([n for n in IT.chain.from_iterable(nodes) if type(n) is Node])

valid_paths = []
while candidates:    
    test_path = []
    check_path(grid, nodes[1][1], '_noparent', nodes[6][6])
 
best_path = min(valid_paths, key=len, default='No valid paths')
print(best_path)

