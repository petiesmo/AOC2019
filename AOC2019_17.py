''' AOC2019 Day 17
Set and Forget
ASCII (Aft Scaffolding and Information Interface)
'''
import Intcode
import logging

class pixel():
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)
		self.char = ''
		self.is_int = False

def get_image(file):
	stream = Intcode(file) 	#Read in ASCII_software
	pixels = stream.read().splitlines()
	
	return tuple([tuple(line) for line in ])

def parse_image(stream):
	image = [chr(s) for s in stream]
	logging.INFO(image) 
	return image
	
def get_nbrs():
	
	return tuple(up,right,down,left)

def get_alignment_params():
	for pixel in pixels:
		if pixel.is_int is True:
			align_param = pixel.x * pixel.y
	

def main():
	ASCII_Software = 'AOC2019_17.ini'
	stream = get_image(ASCII_Software)
	image = parse_image(stream)
	nodes = find_nodes(image)
	align_params = get_alignment_params(image)
	print(f'Calibration is {sum(align_params)}')	#Part A result
	

if __name__ == '__main__':
	main()
