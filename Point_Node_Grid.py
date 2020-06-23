''' Point_Node_Grid.py
Defines classes for grid-like data structures, images, nodes and paths
Default orientation: +X right, +Y down  (consistent with Col/Row and Numpy arrays)
'''

import logging
import itertools as IT

class Point():  
    '''Defines a generic Point data structure to track Location and State information'''
    def __init__(self, x, y, state='-'):
        self.x = x
        self.y = y
        self.state = state
        self.is_node = False
        self.is_path = False
        self.nbrs = get_nbrs(y,x)
    
    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, state={self.state}, node? {self.is_node})'

    @staticmethod
    def get_nbrs(row, col):
            '''Returns a tuple of adjacent cell coordinates (Up,Right,Down,Left)
                Assumes (x right, y down)'''  
            #tpadd = lambda a, b: tuple(m+n for m, n in zip(a, b))
            delr = (-1, 0, 1, 0)
            delc = (0, 1, 0, -1)
            nbrs = [tpadd((row, col), z) for z in zip(delr, delc)]
            return tuple(nbrs)  #(up,right,down,left)
    
    @staticmethod
    def tpadd(a, b):
        return tuple(m+n for m, n in zip(a, b))
        
    #End class Point

class Node(Point):
    '''Special type of Point, with linkage to other nodes in a network'''
    def __init__(self, node_id, x, y):
        self.node_id = node_id
        super().__init__(x, y, 'O')
        self.paths = []
    
    def __repr__(self):
        return f'Node(id:{self.node_id},x:{self.x}, y:{self.y}, paths:{len(self.paths)})'

    #End class Node

class Grid():
    '''2D Array (list of lists) of Point objects, 
    Adjusts Row-Column window to fit x,y extents of Points'''
    
    def __init__(self, points, originxy=(0,0)):
        self.points = points            #Object list (can be sparse)
        self.originxy = originxy       #Maintains translation from row,col to x,y
        self.nodes = []
        self.paths = []
    
    @property
    def array(self):
        a,b,c,d = extents(self)
        return [[0 for p in range(self.ncols)] for row in range(self.nrows)]
    
    @property    
    def extents(self):
        ''' Returns a tuple of x,y coordinates defining corners of a bounding box rectangle'''
        self.xmin = min([p.x for p in self.points])
        self.xmax = max([p.x for p in self.points])
        self.ncols = self.xmax - self.xmin + 1
        self.ymin = min([p.y for p in self.points])
        self.ymax = max([p.y for p in self.points])
        self.nrows = self.ymax - self.ymin + 1
        return None 
    
    @property
    def originrc(self):
        originrc = Point.tpadd((-self.xmin,-self.ymin),self.originxy)
        return self.originrc
        
    def convert_to_rc(self, x, y):
        r = self.originrc + y
        c = self.originrc + x
        return (r,c)
    
    def pad_grid(self,_x,x,_y,y):
        self.array
        return None
    
    def __repr__(self):
        return f'Grid(rows:{self.rows}, cols:{self.cols}, origin:{self.origin})'
    
    def find_nodes(self):
        '''Processing script: accepts an array (list of lists) of points, 
        Checks each point against node criteria
        Modifies Point object is_node value
        Returns a list of Node objects'''
        in_grid = lambda r,c: (r in range(self.rows)) and (c in range(self.cols)) 
        points = [p for p in IT.chain.from_iterable(self)]
        for p in points:
            nbr_vals = [self.array[nr][nc].state if in_grid(nr,nc) else 'NaN' for (nr,nc) in p.nbrs]
            if p.is_scaff:
                p.is_path = nbr_vals[0] == nbr_vals[2] and nbr_vals[1] == nbr_vals[3] and nbr_vals[0] != nbr_vals[1]
                p.is_node = not(is_path)
        ids = IT.count(0)
        return [Node(next(ids), p.x, p.y) for p in points if p.is_node]

    
    def find_paths(self):
        '''Scans a grid of objects row by row, then col by col, looking for 
        node connections (orthogonal paths only)
        Returns tuple of nodes + dict of paths'''
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