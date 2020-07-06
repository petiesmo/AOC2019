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
from Collections import deque
from pprint import pprint
import itertools as IT
from enum import Emum

from Point_Node_Grid import Point, Node, Grid, get_nbrs, tpadd

North = Point(0,1,"^")
East = Point(1,0,'>')
South = Point(0,-1,'v')
West = Point(-1,0,'<')
hdg = deque([North, East, South, West])

class Pixel(Point):
    robot = '<^>v'
    scaffold = '#O' + robot
    
    def __init__(self, x, y, char):
        super().__init__(x, y, state=char)

    @property
    def is_scaff(self):
        return (self.state in self.scaffold)
    
    #End class Pixel

class robot():
	def __init__(self, x, y, hd):
		self.x = x
		self.y = y
		self.hd = hd	#NESW
		path = []
		visited = []
		
	@property
	def pos(self)
		return tuple(self.x, self.y)

	def GoTo(self, grid, dest):
		origin = self.pos
		current = grid[self.y][self.x]
		certain = [origin]
		candidates = 
		while dest not in path:
			#Test fwd
			testxy = tpadd(self.pos,self.hdg)

			#Test L
			hdg.rotate()
			hdg[0]
			if teatxy is node:
				
			#Test R

	
	def move_fwd(self):
		self.visited.append(current_node)
		current_node = new_node
		self.path.append(self.hdg)
		self.x, self.y = new.x, new.y
		return None

	def turn(self):
		
		path.append('L' or 'R')
		return new_hdg

	def choose_next:
		

class ASCII_Comp(Comp_Intcode):
    
    def __init_(self, sw_file):
        super().__init__(sw_file = sw_file)
        self.user_programs = {
			'A': None, #End with \n(10)
			'B': None, 
			'C': None}
		
		self.input_string = IT.chain.fromiterable(self.user_programs.values())
        
    def set_mode_movement(self,move_mode=True):
        self.sw[0] = 2 if move_mode is True else 1
        self.MANUAL_INPUT = not move_mode 
        print(f'ASCII mode successfully switched to {self.sw[0]}')
        return self.sw[0]
        
    def convert_program(program):
        ascii_program = []
        for inst in program:
            ascii_program.extend(ord(inst),ord(','))
        return ascii_program[:-1]
    
    def input_value_generator(self):
        ''' Overrides parent class function to provide specific inputs to the Intcode Computer
        For ASCII Comp, these inputs are program sequences XXXYYYZZZ'''
        something = 0
        return something
    #End class ASCII
    
def get_image(stream):
    ''' Reads a stream of characters,
    and stores data for each new Pixel object
    Returns an array (tuple of tuples) of Pixel objects'''
    screen = ''.join(chr(p) for p in stream).rstrip('\n').splitlines()
    pixels = [[Point(jcol,irow,p) 
           for jcol,p in enumerate(row)] 
           for irow,row in enumerate(screen)]
    #logging.debug(pixels[:][:])
    return tuple((tuple(line) for line in pixels))

def get_nodes(image, state_criteria='*'):
    ids = IT.count(0)
    return [Node(next(ids),p.x,p.y,state='N') 
            for p in IT.chain.from_iterable(image)
            if p.state == state_criteria]

def get_node_nbrs(nodes):
    for n in nodes:
        nbr_coords = get_nbrs(n.y, n.x)
        n.nbrs = [nbr for nbr in nodes if (nbr.y, nbr.x) in nbr_coords]
    return None


def get_alignment_params(nodes):
    '''Finds intersections and returns tuple of (Pixel, AlignParam) pairs'''
    return tuple([(n, n.x*n.y) 
                   for n in nodes
                   if len(n.nbrs) == 4])
    
def read_input(file):
    with open(file,'r') as f:
        stream = f.read()
    return stream

def find_path(nodes, startpt):
	network = nodes[:]
	if any([len(e.nbrs)== 0 for e in network]): 
		print('Isolated node found')
        
    endpts = [e for e in network if len(e.nbrs) == 1]
    if len(endpts) > 2:
        print('More than one start/end')
    
    opennodes = network[:]
    closednodes = []
    current_node = startpt
    previous_node = None
    while current_node != end_node
        current_node.parent = previous_node
        previous_node, current_node = current_node, current_node.nbrs

	for nbr in current_node.nbrs:
		if nbr in opennodes
	

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
    ASCII_Software = 'AOC2019_17.ini'
    AC1 = ASCII_Comp(sw_file=ASCII_Software)
    AC1.LOOP_compute_until_output_or_stop(stop_at_each_output=False)
    data_stream = AC1.memory[:]
    image = get_image(data_stream)
    pprint([''.join([p.state for p in row]) for row in image]) 
    nodes = get_nodes(image)
    pprint(nodes)
    robot_pos = [(p.y,p.x) for p in image if p.state in Pixel.robot]
    path = find_path(nodes,robot_pos)
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
    nodes = get_nodes(image)
    pprint(nodes)
    get_node_nbrs(nodes)
    print([(node.y,node.x,len(node.nbrs)) for node in nodes])

if __name__ == '__main__':
    #test1()
    mainA()
    #test2()
    #mainB()
