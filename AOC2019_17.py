''' AOC2019 Day 17 - Set and Forget
ASCII (Aft Scaffolding and Information Interface)
Part A: Find alignment parameters of scaffolding intersections
Part B: 
'''
''' Character representations:
'.' = Space, '#' = Scaffold, 'o' = Intersection
<,^,>,v = Robot location + direction
X = Robot falls into space
'''
from IntcodeComp import Comp_Intcode 
import logging
from collections import namedtuple
from pprint import pprint
import itertools as IT

class Pixel():
    robot = '<^>v'
    scaffold = '#O' + robot
    
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.is_node = False
        self.is_cross = False
        self.is_corner = False
        self.nbrs = ()
    
    def __repr__(self):
        return f'Pixel(x = {self.x}, y = {self.y}, char = {self.char})'

    @property
    def is_scaff(self):
        return True if self.char in self.scaffold else False

    def check_if_node(self, grid):
        rows, cols = len(grid), len(grid[0])
        in_grid = lambda r,c: (r in range(rows)) and (c in range(cols)) 

        self.nbrs = get_nbrs(self.y, self.x)
        nbr_vals = [grid[nr][nc].char if in_grid(nr,nc) else 'NaN' for (nr,nc) in self.nbrs]
        
        self.is_cross = self.is_scaff and all([v in self.scaffold for v in nbr_vals])
        self.is_corner = self.is_scaff and not self.is_cross and any([v in self.scaffold and v==nbr_vals[i-1] for i,v in enumerate(nbr_vals)])
        self.is_node = self.is_cross or self.is_corner
        logging.debug(f'(self.y,self.x) N,+,L = {self.is_node, self.is_cross, self.is_corner}')
        return self.is_node

def get_image(stream):
    ''' Runs the input software into the Intcode computer, reads output stream,
    and stores data for each new Pixel object
    Returns an array (tuple of tuples) of Pixel objects'''
    screen = ''.join(chr(p) for p in stream).rstrip('\n').splitlines()
    pixels = [[Pixel(jcol,irow,p) 
           for jcol,p in enumerate(row)] 
           for irow,row in enumerate(screen)]
    #logging.debug(pixels[:][:])
    return tuple((tuple(line) for line in pixels))

def get_nbrs(row,col):
        '''Returns a tuple of adjacent cell values (Up,Right,Down,Left)
            Assumes origin is at Upper Left'''  
        tpadd = lambda a,b: tuple(m+n for m,n in zip(a,b))
        delr = (-1,0,1,0)
        delc = (0,1,0,-1)
        nbrs = [tpadd((row,col),z) for z in zip(delr,delc)]
        return tuple(nbrs)  #(up,right,down,left)
    
def get_alignment_params(grid):
    '''Finds intersections and returns tuple of (Pixel, AlignParam) pairs'''
    return tuple([(pixel, pixel.x*pixel.y) 
                    for pixel in IT.chain.from_iterable(grid) 
                    if pixel.is_cross is True])
    
def read_input(file):
    with open(file,'r') as f:
        stream = f.read()
    return stream

def main():
    logfile = 'AOC2019_17.log'
    logging.basicConfig(level=logging.INFO, file=logfile, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    ASCII_Software = 'AOC2019_17.ini'
    ASCII_Comp = Comp_Intcode(sw_file=ASCII_Software)
    ASCII_Comp.LOOP_compute_until_output_or_stop(stop_at_each_output=False)
    stream = ASCII_Comp.memory[:]
    image = get_image(stream)
    pprint([''.join([p.char for p in row]) for row in image])
    pixels = [p for p in IT.chain.from_iterable(image)]
    for p in pixels:
        p.check_if_node(image)
    intersections = get_alignment_params(image)
    print(f'Calibration is {sum([ap for pixel,ap in intersections])}')  #Part A result
    logging.info(f'Calibration is {sum([ap for pixel,ap in intersections])}')  #Part A result: 3336
                  
def test():
    logfile = 'AOC2019_17Test.log'
    logging.basicConfig(level=logging.DEBUG, filename=logfile, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    test_input = 'AOC2019_17.test'
    stream = [ord(c) for c in read_input(test_input)]
    image = get_image(stream)
    pprint([[p.char for p in row] for row in image])
    pixels = [p for p in IT.chain.from_iterable(image)]
    for p in pixels:
        p.check_if_node(image)
    intersections = get_alignment_params(image)
    print(intersections)
    print(f'Calibration is {sum([ap for (pixel,ap) in intersections])}')  #Part A result: 76
    
if __name__ == '__main__':
    main()
    #test()
