''' Point_Node_Grid.py
Defines classes for grid-like data structures, images, nodes and paths
Default orientation: +X right, +Y down  (consistent with Col/Row and Numpy arrays)
Assumption: Each point along path is a Node, with path (length = 1) to neighbors
'''

import logging
import itertools as IT
from pprint import pprint

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
    '''Defines a generic Point data structure to track Location and State information'''
    def __init__(self, x, y, state=False, **kwargs):
        self.x = x
        self.y = y
        self.state = state
        self.__dict__.update(kwargs)
    
    @property
    def pos(self):
        return tuple(self.x, self.y)

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, state={self.state})'

    def __add__(self, other):
        return (self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def dist(self, other, crow=True):
        if crow:    #Euclidian
            return ((self.x-other.x)**2 + (self.y - other.y)**2)**.5
        else:       #Manhattan
            return abs(self.x-other.x) + abs(self.y-other.y)         
    #End class Point


class Node(Point):
    '''Special type of Point, with linkage to other nodes in a network'''
    def __init__(self, node_id, x, y, state=False):
        super().__init__(x, y, state=state, node_id=node_id, nbrs=[], paths=[], parent=None)
    
    def __repr__(self):
        return f'Node(id:{self.node_id},x:{self.x}, y:{self.y})'

    #End class Node

class Grid():
    '''2D Array (list of lists) of Point objects, 
    Adjusts Row-Column window to fit x,y extents of Points'''
    
    def __init__(self, points, originxy=(0,0)):
        self.points = list(IT.chain.from_iterable(points))           #Object list or array (can be sparse)
        self.originxy = originxy       #Maintains translation from row,col to x,y
        self.origin = Point(*self.originxy, state='*')
        self.nodes = []
        self.paths = []
    
    @property
    def array(self):
        self.find_extents()
        array = [[None for col in range(self.ncols)] for row in range(self.nrows)]
        for p in self.points:
            r,c = self.convert_to_rc(p.x,p.y)
            array[r][c] = p
        return array
        
    def find_extents(self):
        ''' Returns a tuple of x,y coordinates defining corners of a bounding box rectangle'''
        self.xmin = min([p.x for p in self.points])
        self.xmax = max([p.x for p in self.points])
        self.ncols = self.xmax - self.xmin + 1
        self.ymin = min([p.y for p in self.points])
        self.ymax = max([p.y for p in self.points])
        self.nrows = self.ymax - self.ymin + 1
        x0,y0 = self.originxy
        self.originrc = (y0-self.ymin,x0-self.xmin)
        return None 
        
    def convert_to_rc(self, x, y):
        r, c = self.originrc
        r = y - self.ymin
        c = x - self.xmin
        return (r, c)

	def getxy(self, x, y):
		''' Retreive object stored at x,y'''
		r,c = convert_to_rc(x,y)
		return self.array[r][c]
    
    def pad_grid(self, negx, posx, negy, posy):
        ''' Future implementation'''
        return None
    
    def __repr__(self):
        return f'Grid(rows:{self.nrows}, cols:{self.ncols}, origin:{self.originrc})'

    def find_nodes(self, state_criteria='*'):
        '''Processing script:
        Checks each point against node criteria.  Populates list of Node objects'''	
        ids = IT.count(0)
        self.nodes = [Node(next(ids),p.x,p.y,state=p.state) for p in self.points if p.state in state_criteria]
        return None

    def get_node_nbrs(self):
        for n in self.nodes:
            nbr_coords = get_nbrs(n.y, n.x)
            n.nbrs = [nbr for nbr in self.nodes if (nbr.y, nbr.x) in nbr_coords]
        return None

    def find_network(self):
        '''Scans a grid of objects row by row, then col by col, looking for 
        node connections (orthogonal paths only) at intersections/ends
        Returns tuple of nodes + dict of links'''
        links = IT.count(0)
        grid = self.array
        #Check linkage between adjacent nodes horizontally
        for i, point_row in enumerate(grid):
            node_row = [n for n in nodes if n.row == i]
            for n in range(1, len(node_row)):
                nodeL, nodeR = node_row[n-1], node_row[n]
                span = point_row[nodeL.col+1 : nodeR.col]
                if all([p.is_scaff for p in span]):
                    link = next(links)
                    paths[link] = ('H', len(span), nodeL.node_id, nodeR.node_id)
                    nodeL.paths.append((link, len(span), nodeR.node_id))
                    nodeR.paths.append((link, len(span), nodeL.node_id))

        #Check linkage between adjacent nodes vertically
        for i,p in enumerate(grid[0]):
            point_col = [row[i] for row in grid]
            node_col = [n for n in nodes if n.col == i]        
            for n in range(1, len(node_col)):
                nodeL, nodeR = node_col[n-1], node_col[n]
                span = point_col[nodeL.col+1 : nodeR.col]
                if all([p.is_scaff for p in span]):
                    link = next(links)
                    paths[link] = ('V', len(span), nodeL.node_id, nodeR.node_id)
                    nodeL.paths.append((link, len(span), nodeR.node_id))
                    nodeR.paths.append((link, len(span), nodeL.node_id))
        return tuple(nodes), paths
    #End class Grid


def test():
    points = [Point(x,y,'.') for y in range(-6,2,1) for x in range(-2,8,1)]
    #pprint(points)

    grid = Grid(points)
    image = grid.array
    print(grid.originxy, grid.originrc)
    pprint([[p.state for p in row] for row in image])

if __name__ == "__main__":
    test()    