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
from pprint import pprint
import itertools as IT

from Point_Node_Grid import Point,Node,Grid

class Pixel(Point):
    robot = '<^>v'
    scaffold = '#O' + robot
    
    def __init__(self, x, y, char):
        super().__init__(x,y,state=char)

    @property
    def is_scaff(self):
        return (self.char in self.scaffold)
    
    #End class Pixel

class ASCII_Comp(Comp_Intcode):
    
    def __init_(self, sw):
        super().__init__(sw_file = sw)
        self.programs = {1: None, 2: None, 3: None}
        
        
    def switch_ASCII_mode(movement=False):
        self.sw[0] = XX if movement is True else XX
        self.MANUAL_INPUT = False
        print(f'ASCII mode successfully switched to {self.sw[0]}')
        return self.sw[0]
        
    def convert_program(program):
        ascii_program = []
        for inst in program:
            ascii_program.extend(ord(inst),ord(','))
        return ascii_program
    
    def input_value_generator(self):
        ''' Overrides parent class function to provide specific inputs to the Intcode Computer
        For ASCII Comp, these inputs are program sequences XXXYYYZZZ'''
        something = 0
        return something
    #End class ASCII
    
def get_image(stream):
    ''' Runs the input software into the Intcode computer, reads output stream,
    and stores data for each new Pixel object
    Returns an array (tuple of tuples) of Pixel objects'''
    screen = ''.join(chr(p) for p in stream).rstrip('\n').splitlines()
    pixels = [[Point(jcol,irow,p) 
           for jcol,p in enumerate(row)] 
           for irow,row in enumerate(screen)]
    #logging.debug(pixels[:][:])
    return tuple((tuple(line) for line in pixels))
 
def get_alignment_params(grid):
    '''Finds intersections and returns tuple of (Pixel, AlignParam) pairs'''
    return tuple([(pixel, pixel.x*pixel.y) 
                    for pixel in IT.chain.from_iterable(grid) 
                    if pixel.is_cross is True])
    
def read_input(file):
    with open(file,'r') as f:
        stream = f.read()
    return stream

def mainA():
    #logfile = 'AOC2019_17.log'
    #logging.basicConfig(level=logging.INFO, file=logfile, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
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
     
def mainB():
    ASCII_Software = 'AOC2019_17.ini'
    AC1 = ASCII_Comp(sw_file=ASCII_Software)

     
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

def test2():
    test_input = '..#..........\n..#..........\n#######...###\n#.#...#...#.#\n#############\n..#...#...#..\n..#####...^..'
    stream = [ord(c) for c in test_input]
    image = get_image(stream)
    pprint([[p.char for p in row] for row in image]) 
    pixels = [p for p in IT.chain.from_iterable(image)] 
    for p in pixels:
        p.check_if_node(image)
    print(len(pixels))
    pprint(pixels)
    nodes, paths = Grid.build_network(image)

if __name__ == '__main__':
    #main()
    test2()
