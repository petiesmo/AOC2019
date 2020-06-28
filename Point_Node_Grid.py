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
    
    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, state={self.state})'
        
    #End class Point


class Node(Point):
    '''Special type of Point, with linkage to other nodes in a network'''
    def __init__(self, node_id, x, y, state=False):
        super().__init__(x, y, state=state, node_id=node_id, nbrs=[], parent=None)
    
    def __repr__(self):
        return f'Node(id:{self.node_id},x:{self.x}, y:{self.y})'

    #End class Node

class Grid():
    '''2D Array (list of lists) of Point objects, 
    Adjusts Row-Column window to fit x,y extents of Points'''
    
    def __init__(self, points, originxy=(0,0)):
        self.points = points           #Object list (can be sparse)
        self.originxy = originxy       #Maintains translation from row,col to x,y
        self.nodes = [originxy]
        self.paths = []
    
    @property
    def array(self):
        self.find_extents()
        array = [['NaN' for col in range(self.ncols)] for row in range(self.nrows)]
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
        self.originrc = tpadd((-self.xmin,-self.ymin), self.originxy)
        return None 
        
    def convert_to_rc(self, x, y):
        r,c = self.originrc
        r = y - self.ymin
        c = x - self.xmin
        return (r,c)
    
    def pad_grid(self,negx,posx,negy,posy):
        ''' Future implementation'''
        return None
    
    def __repr__(self):
        return f'Grid(rows:{self.nrows}, cols:{self.ncols}, origin:{self.originrc})'
    
    def find_nodes(self):
        '''Processing script: accepts an array (list of lists) of points, 
        Checks each point against node criteria
        Modifies Point object is_node value
        Returns a list of Node objects'''
        in_grid = lambda r,c: (r in range(self.nrows)) and (c in range(self.ncols)) 
        ids = IT.count(0)
        self.nodes = [Node(next(ids), p.x, p.y) for p in self.points]
        for n in self.nodes:
            n.nbrs = [self.array[nr][nc] if in_grid(nr,nc) and self.array[nr,nc].is_node else 'NaN' for (nr,nc) in p.nbrs]
        
        return 
    #End class Grid


def test():
    points = [Point(x,y,'.') for y in range(-6,4,2) for x in range(-2,8,2)]
    pprint(points)

    grid = Grid(points)
    pprint(grid.array)
    print(grid.originxy, grid.originrc)

if __name__ == "__main__":
    test()    