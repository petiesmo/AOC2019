''' AOC2019 Day 17 - Set and Forget
ASCII (Aft Scaffolding and Information Interface)
Part A: Find alignment parameters of scaffolding intersections
Part B: 
'''
from IntcodeComp import Comp_Intcode 
import logging
from collections import namedtuple
from pprint import pprint

Pixel = namedtuple('Pixel', 'x y char is_cross is_corner')
scaffold = ['#o']
robot = ['<^>vx']
''' Character representations:
'.' = Space, '#' = Scaffold, 'o' = Intersection
<,^,>,v = Robot location + direction
X = Robot falls into space
'''

def get_image(stream):
    ''' Runs the input software into the Intcode computer, reads output stream,
    and stores data for each new Pixel object
    Returns an array (tuple of tuples) of Pixel objects'''
    screen = stream.splitlines()
    pixels = [[Pixel(jcol,irow,chr(p),False,False) 
           for jcol,p in enumerate(row)] 
           for irow,row in enumerate(screen)]
    #logging.DEBUG(pixels[:][:])
    return tuple((tuple(line) for line in pixels))

def get_nbrs(pixel):
        '''Returns a tuple of adjacent cell values (Up,Right,Down,Left)'''  
        r,c = pixel.y, pixel.x
        tpadd = lambda a,b: tuple(m+n for m,n in zip(a,b))
        rs = (-1,0,1,0)
        cs = (0,1,0,-1)
        nbrs = [tpadd((r,c),z) for z in zip(rs,cs)]
        return tuple(nbrs)  #(up,right,down,left)

def find_nodes(grid):
    rows, cols = len(grid), len(grid[0])
    for row in grid:
        for pixel in row:
            nbrs = get_nbrs(pixel)
            in_grid = lambda r,c: (r in range(rows)) and (c in range(cols)) 
            is_cross = lambda val: all([i == '#' for i in val])
            is_corner = lambda val: not pixel.is_cross and any([val[i] == val[i-1] == '#' for i,v in enumerate(val)])
            vals = [grid[nr][nc] if in_grid(nr,nc) else 'NaN' for (nr,nc) in nbrs]
            pixel = Pixel(pixel.x, pixel.y, pixel.char, is_cross(vals),is_corner(vals))
    pprint(f'{["".join([pixel.char for pixel in row]) for row in grid]}')
    pprint(f'{[[pixel.is_cross for pixel in row] for row in grid]}')
    pprint(f'{[[pixel.is_corner for pixel in row] for row in grid]}')
    
def get_alignment_params(grid):
    '''Finds intersections and returns tuple of (Pixel, AlignParam) pairs'''
    ints = []
    for row in grid:
                for pixel in row:
                        if pixel.is_cross is True:
                                align_param = pixel.x * pixel.y
                                ints.append((pixel,align_param))
    return tuple(ints)
    
def read_input(file):
    with open(file,'r') as f:
        stream = f.read()
    return stream

def main():
    logfile = 'AOC2019_17.log'
    logging.basicConfig(level = logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    ASCII_Software = 'AOC2019_17.ini'
    ASCII_Comp = Comp_Intcode(sw_file=ASCII_Software)
    ASCII_Comp.LOOP_compute_until_output_or_stop(stop_at_each_output=False)
    stream = ASCII_Comp.memory[:]
    image = get_image(stream)
    nodes = find_nodes(image)
    intersections = get_alignment_params(image)
    print(f'Calibration is {sum([ap for pixel,ap in intersections])}')  #Part A result

def test():
    logfile = 'AOC2019_17Test.log'
    logging.basicConfig(level = logging.DEBUG, filename = logfile, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    test_input = 'AOC2019_17.test'
    stream = (ord(c) for c in read_input(test_input))
    image = get_image(stream)
    nodes = find_nodes(image)
    intersections = get_alignment_params(image)
    print(f'Calibration is {sum([ap for pixel,ap in intersections])}')  #Part A result
    
if __name__ == '__main__':
    #main()
    test()
