''' Pixel_Node_Grid.py
Defines classes for grid-like data structures, images, nodes and paths
Default orientation: +X right, +Y down  (consistent with Col/Row and Numpy arrays)
'''

import logging
import itertools as IT

class Pixel():
    robot = '<^>v'
    scaffold = '#O' + robot
    
    def __init__(self, x, y, char='.'):
        self.x = x
        self.y = y
        self.char = char
        self.is_node = False
        self.is_path = False
        self.nbrs = get_nbrs(y,x)
    
    def __repr__(self):
        return f'Pixel(x={self.x}, y={self.y}, char={self.char}, node? {self.is_node})'

    @property
    def is_scaff(self):
        return (self.char in self.scaffold)

    @staticmethod
    def get_nbrs(row, col):
            '''Returns a tuple of adjacent cell coordinates (Up,Right,Down,Left)
                Assumes (x right, y down)'''  
            tpadd = lambda a, b: tuple(m+n for m, n in zip(a, b))
            delr = (-1, 0, 1, 0)
            delc = (0, 1, 0, -1)
            nbrs = [tpadd((row, col), z) for z in zip(delr, delc)]
            return tuple(nbrs)  #(up,right,down,left)
    #End Class Pixel

class Node(Pixel):
    def __init__(self, node_id, x, y):
        self.node_id = node_id
        super().__init__(x, y, 'O')
        self.paths = []
    
    def __repr__(self):
        return f'Node(id:{self.node_id},x:{self.x}, y:{self.y}, paths:{len(self.paths)})'

    #End Node class

class Grid():
    def __init__(self, rows, cols, origin=(0,0), default=int(0)):
        self.rows = rows
        self.cols = cols
        self.origin = origin    #Translation from row,col to x,y    
        self.array = [[default for c in cols] for r in rows]
    
    @property    
    def extents(self):
        ''' Returns a tuple of x,y coordinates defining corners of a bounding box rectangle'''
        xmin,xmax = -self.origin[1], self.cols
        ymin,ymax = self.rows, self.rows
        return tuple((xmin,ymax),(xmax,ymin)) 
    
    def pad_grid(self,_x,x,_y,y):
        self.array
        return None
    
    def __repr__(self):
        return f'Grid(rows:{self.rows}, cols:{self.cols}, origin:{self.origin})'
    
    def find_nodes(self):
        '''Processing script: accepts an array (list of lists) of pixels, 
        checks each pixel against node criteria
        Modifies Pixel object is_node value
        Returns a list of Node objects'''
        in_grid = lambda r,c: (r in range(self.rows)) and (c in range(self.cols)) 
        pixels = [p for p in IT.chain.from_iterable(self)]
        for p in pixels:
            nbr_vals = [self.array[nr][nc].char if in_grid(nr,nc) else 'NaN' for (nr,nc) in p.nbrs]
            if p.is_scaff:
                p.is_path = nbr_vals[0] == nbr_vals[2] and nbr_vals[1] == nbr_vals[3] and nbr_vals[0] != nbr_vals[1]
                p.is_node = not(is_path)
        ids = IT.count(0)
        return [Node(next(ids), p.x, p.y) for p in pixels if p.is_node]

    @staticmethod
    def build_network(grid):
        '''Scans a grid of objects row by row, then col by col, looking for 
        node connections (orthogonal paths only)
        Returns tuple of nodes + dict of paths'''
        
        links = IT.count(0)
        paths = {}
        nodes = 
        #Check linkage between adjacent nodes horizontally
        for i, pixel_row in enumerate(grid):
            node_row = [n for n in nodes if n.row == i]
            for n in range(1, len(node_row)):
                nodeL, nodeR = node_row[n-1], node_row[n]
                span = pixel_row[nodeL.col+1 : nodeR.col]
                if all([p.is_scaff for p in span]):
                    link = next(links)
                    paths[link] = ('H', len(span), nodeL.node_id, nodeR.node_id)
                    nodeL.paths.append((link, len(span), nodeR.node_id))
                    nodeR.paths.append((link, len(span), nodeL.node_id))

        #Check linkage between adjacent nodes vertically
        for i,p in enumerate(grid[0]):
            pixel_col = [row[i] for row in grid]
            node_col = [n for n in nodes if n.col == i]        
            for n in range(1, len(node_col)):
                nodeL, nodeR = node_col[n-1], node_col[n]
                span = pixel_col[nodeL.col+1 : nodeR.col]
                if all([p.is_scaff for p in span]):
                    link = next(links)
                    paths[link] = ('V', len(span), nodeL.node_id, nodeR.node_id)
                    nodeL.paths.append((link, len(span), nodeR.node_id))
                    nodeR.paths.append((link, len(span), nodeL.node_id))
        return tuple(nodes), paths
