''' AOC2019 Day 17 - Set and Forget
ASCII (Aft Scaffolding and Information Interface)
Part A: Find alignment parameters of scaffolding intersections
Part B: Write program segments A,B,C to navigate robot on all scaffolds
'''
''' Character representations:
'.' = Space, '#' = Scaffold, 'o' = Intersection
<,^,>,v = Robot location + direction
X = Robot falls into space
'''
''' Part B program segment requirements:
Comprised of ASCII characters, representing turns (L/R), fwd steps (integer), commas, and a newline
3 Segments (A/B/C): No more than 20 characters (including commas, but not newline)
Main movement routine: Calls A/B/C segments
'''
from IntcodeComp import Comp_Intcode 
from Collections import deque
from pprint import pprint
import itertools as IT
import re

from Point_Node_Grid import Point, Node, Grid, get_nbrs, tpadd

North = Point(0,1,"^")
East = Point(1,0,'>')
South = Point(0,-1,'v')
West = Point(-1,0,'<')
hdgs = deque([North, East, South, West])

ROBOT = '^>v<'
SCAFFOLD = '#O' + ROBOT
MAX_LENGTH = 20

class Pixel(Point):
    def __init__(self, x, y, char):
        super().__init__(x, y, state=char)

    @property
    def is_scaff(self):
        return self.state in SCAFFOLD
    
#End class Pixel

class Robot(Point):
    def __init__(self, x, y, heading):
        super().__init__(x, y, state='Start', char=heading)
        self.path = []
        self.visited = []
        self._hdg = hdgs.copy()
        while self.hdg.state != heading:
            self.turn('L')
    @property
    def char(self):
        return self._hdg[0].state
    @property
    def hdg(self):
        return self._hdg[0]

    def turn(self, LR='L'):
        if LR == 'L':
            self._hdg.rotate()
        elif LR == 'R':
            self._hdg.rotate(-1)
        else:
            raise ValueError('L or R only')
        return new_hdg

    @hdg.setter
    def hdg(self, URDL=None):         
        if URDL is not None:
            while self.char != URDL:
                self.turn('L')
        return None

    def follow_a_path(self, grid, destination):
        ''' Robot method to follow a chalk line path; 
            Prefers to go forward before looking to turn'''
        #TODO: Finish implementing this method for the robot
        not_visited = grid.nodes[:]
        trail = []

        while not_visited and (self.pos not destination):
			test_coord = self + self.hdg
			if any([n.pos == test_coord for n in current_node.nbrs]):
				not_visited.remove(current_node))
                trail.append('F')
                self.pos = test_coord
				current_node = grid[self.y][self.x]
            else:
                self.trail.append('L')
                self.turn()


    def convert_trail(seq):
        '''Condenses repeated steps in the Trail attribute'''
        # 3 lefts = 1 right
        # Fwd, Fwd, Fwd, ....  = Integer
        short_list = []
        step = [seq[0]]
        for i in seq[1:]:
            if i == step[0]:
                step.append(i)
            else:
                short_list.append((step[0],len(step)))
                step = [i]
                #print(short_list)
        short_list.append((step[0],len(step)))
        
        new_trail = []
        for grp in short_list:
            if grp[0] == 'Fwd':
                new_trail.append(grp[1])
            elif grp == ('Left',3):
                new_trail.append('R')
            else:
                new_trail.append('L')
                
        return new_trail
# End Class Robot    

class ASCII_Comp(Comp_Intcode):
    def __init_(self, sw_file):
        super().__init__(sw_file = sw_file)
        self.user_programs = {
            'MMR': None #Main move routine
            'A': None, #End with \n(10)
            'B': None, 
            'C': None}

        self.input_string = IT.chain.fromiterable(self.user_programs.values())
        
    def set_mode_movement(self, move_mode=True):
        self.sw[0] = 2 if move_mode is True else 1
        self.MANUAL_INPUT = not move_mode 
        print(f'ASCII mode successfully switched to {self.sw[0]}')
        return self.sw[0]

    def convert_user_program(program):
        '''User program segments are fed to the Intcode computer as a list of
        ASCII characters (including the commas) and a newline'''
        ascii_program = []
        for inst in program:
            ascii_program.append(ord(inst))
            ascii_program.append(ord(','))
        ascii_program.append(ord('\n'))
        return ascii_program
    
    def input_value_generator(self):
        ''' Overrides parent class function to provide specific inputs to the Intcode Computer
        For ASCII Comp, these inputs are program sequences XXXYYYZZZ'''
        #TODO Update the exact feed into the Intcode comp (it's close)
        movement_programs = IT.chain.from_iterable(self.user_programs.values())
        return next(movement_programs)
#End class ASCII_Comp


def find_move_patterns(trail):
        ''' Looks for repeated patterns in the trail stream, returns 3 groupings'''
        # A begins with first 2 movements (or more)
        # C ends with last 2 movements (or more)
        #TODO Implement algorithm to extract move pattern groups (use regex)
        trail_str = ','.join([str(i) for i in trail])
        for seq_length in range(MAX_LENGTH,2,-1):
            seq = trail_str[:seq_length]
            avail = trail_str[seq_length:]
			matches = re.finditer()
			
			if len(matches):
				A = seq
				re.split(matches,trail_str)
		MAXB = 
		for seq_length in range(
			
        return A,B,C,seq 

def get_image(stream):
    ''' Reads a stream of characters,
    and stores data for each new Pixel object
    Returns an array (tuple of tuples) of Pixel objects'''
    screen = ''.join(chr(p) for p in stream).rstrip('\n').splitlines()
    pixels = [[Pixel(jcol,irow,p) 
           for jcol,p in enumerate(row)] 
           for irow,row in enumerate(screen)]
    #logging.debug(pixels[:][:])
    return tuple((tuple(line) for line in pixels))

def get_alignment_params(nodes):
    '''Finds intersections and returns tuple of (Pixel, AlignParam) pairs'''
    return tuple([(n, n.x*n.y) for n in nodes if len(n.nbrs) == 4])
    
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
    pprint([''.join([p.state for p in row]) for row in image])
    nodes = get_nodes(image, '#')
    get_node_nbrs(nodes)
    intersections = get_alignment_params(nodes)
    print(f'Calibration is {sum([ap for pixel,ap in intersections])}')  #Part A result
    #logging.info(f'Calibration is {sum([ap for pixel,ap in intersections])}')  #Part A result: 3336


def mainB():
    ''' Driving code for Day17 Part B'''
    ASCII_Software = 'AOC2019_17.ini'
    AC1 = ASCII_Comp(sw_file=ASCII_Software)
    AC1.LOOP_compute_until_output_or_stop(stop_at_each_output=False)
    data_stream = AC1.memory[:]
    image = Grid(get_image(data_stream))
    pprint([''.join([p.state for p in row]) for row in image]) 

    image.get_nodes(state_criteria='#<^>v')
    bot = [Robot(n.x,n.y,state=n.state) for n in image.nodes if n.state in ROBOT][0]
    get_node_nbrs(nodes)
    pprint(nodes,bot)

    for n in nodes:
        image[n.y][n.x] = n
        if len(n.nbrs) == 1 and n.state == '#':
            endpt = n

    bot.GoTo(image, endpt)
    trail = bot.trail
    short_trail = bot.convert_trail(trail)
    patterns = bot.find_move_patterns(short_trail)
    bot.

    AC1.set_mode_movement(move_mode=True)
    AC1.convert_user_program()

    
#make_directions
#make_movement_programs
#make_main_movement_routine
#run_MMR

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
    data_stream = [ord(c) for c in test_input]
    image = get_image(data_stream)
    pprint([''.join([p.state for p in row]) for row in image]) 
    nodes = get_nodes(image, '#')
    pprint(nodes)
    get_node_nbrs(nodes)
    print([(node.y,node.x,len(node.nbrs)) for node in nodes])

if __name__ == '__main__':
    #test1()
    mainA()
    #test2()
    #mainB()
