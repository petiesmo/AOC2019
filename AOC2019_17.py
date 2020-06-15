''' AOC2019 Day 17
Set and Forget
ASCII (Aft Scaffolding and Information Interface)
Part A: Find alignment parameters of scaffolding intersections
Part B: 
'''
import Intcode
import logging
from collections import namedtuple

Pixel = namedtuple('Pixel', 'x y char is_int')
''' Character representations:
'.' = Space
'#' = Scaffold
'o' = Intersection
<,^,>,v = Robot location + direction
X = Robot falls into space
'''

def get_image(stream):
	''' Runs the input software into the Intcode computer, reads output stream,
	and stores data for each new Pixel object
	Returns an array (tuple of tuples) of Pixel objects'''
	screen = stream.splitlines()
	pixels = [[Pixel(jcol,irow,chr(p),False) 
		   for jcol,p in enumerate(row)] 
		   for irow,row in enumerate(screen)]
	logging.DEBUG(pixels)
	return tuple((tuple(line) for line in pixels))

def get_nbrs():
	'''Returns a tuple of adjacent cell values (Up,Right,Down,Left)'''	
	return tuple(up,right,down,left)

def get_alignment_params(image):
	'''Finds intersections and returns tuple of (Pixel, AlignParam) pairs'''
	ints = []
	for pixel in image:
		if pixel.is_int is True:
			align_param = pixel.x * pixel.y
			ints.append((pixel,align_param))
	return tuple(ints)
	
def read_input(file):
	with open(test_input,'r') as f:
		stream = f.read()
	return stream

def main():
	logfile = 'AOC2019_17.log'
	logging.basicConfig(level = logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	ASCII_Software = 'AOC2019_17.ini'
	sw = read_input(ASCII_Software)
	stream = Intcode(sw) 		#Process ASCII_software through Intcode computer
	image = get_image(stream)
	nodes = find_nodes(image)
	intersections = get_alignment_params(image)
	print(f'Calibration is {sum([ap for pixel,ap in intersections])}')	#Part A result

def test():
	logfile = 'AOC2019_17Test.log'
	logging.basicConfig(level = logging.DEBUG, filename = logfile, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	test_input = 'AOC2019_17.test'
	stream = read_input(test_input)
	image = get_image(stream)
	nodes = find_nodes(image)
	intersections = get_alignment_params(image)
	print(f'Calibration is {sum([ap for pixel,ap in intersections])}')	#Part A result
	
if __name__ == '__main__':
	#main()
	test()
