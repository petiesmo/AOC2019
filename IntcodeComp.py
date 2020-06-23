# -*- coding: utf-8 -*-
"""
Mar 2020
@author: pjsmole
Advent of Code 2019
Defines multi-use Intcode Computer class 
"""
from copy import deepcopy
import logging
import sys

#logfile = 'C:\\Reports\\AOC197.log'

class Comp_Intcode:
    '''
    Core methods and constants for the Intcode computer. 
    Software (codestring) is called and run, returning an output
    '''
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(message)s', 
                        datefmt = '%Y-%m-%d %H:%M:%S') #, stream = sys.stdout)
    logging.debug("Test Message")

    MANUAL_INPUT = True
    
    def __init__(self, sw_file=None, startpos=0, startbase=0, **kwargs):
        codestring = self.read_software(sw_file)
        self.__sw_ref = tuple(deepcopy(codestring)) # Store initial state & final state
        self.sw = list(deepcopy(codestring))       # May vary with runtime commands
        self.curpos = int(startpos)
        self.relbase = int(startbase)
        self.memory = ()
        #self.Comp_Output = None
        logging.debug('New Intcode Computer set up! {self.__name__}')
    
    def __repr__(self):
        return f'Comp_Intcode(curpos={self.curpos}, code={self.sw[self.curpos]}, relbase={self.relbase})'

    def read_software(self, filename=None):
        ''' Ingests a comma-separated string of commands from a text file
            Returns a list of commands (string format)'''
        if filename is None:
            return ('109','1','203','6','4','7','99')
        else:
            with open(filename, mode='r', encoding='ANSI') as f:
                codestring = f.read().replace('\n','').split(sep=",")
            return codestring

    @property
    def sw_ref(self):
        return self.__sw_ref[:]

    @property
    def sw(self):
        return self._sw[:]
    @sw.setter
    def sw(self, new_sw=None):    
        if new_sw is not None:
            self._sw = new_sw
        return None

    def set_sw_pos(self, pos=None, set_value=None):
        '''Checks validity (negative position values not allowed),
         extends codestring to new position, if beyond current length,
         and sets new value at position (if specified)'''
        pos = int(pos)
        if self.check_sw_pos(pos) is False:
            # Extend the codestring!
            for n in range(len(self.sw), pos+1):
                self._sw.append(0)
            logging.debug(self.sw)
        # Update the value
        if set_value is not None:
            self._sw[pos] = str(set_value)
        return None

    def check_sw_pos(self, pos=None):
        '''Checks validity (negative position values not allowed)'''
        pos = int(pos)
        if pos < 0:
            raise ValueError
        elif pos >= len(self._sw):
            return False
        else:
            return True

    @property
    def curpos(self):
        return self._curpos
    @curpos.setter
    def curpos(self, new_pos=None):
        if new_pos is not None:
            self._curpos = int(new_pos)
        return None
        
    @property
    def relbase(self):
        return self._relbase
    @relbase.setter
    def relbase(self, newbase=None):
        if newbase is not None:
            self._relbase = int(newbase)
            return int(newbase)
        return None

    @property
    def memory(self):
        return self._memory
    @memory.setter
    def memory(self, write_mem=None):
        if write_mem is not None:
            self._memory = tuple(write_mem)
        return None 

    def write_value_to_memory(self, new_value=None):
        if new_value is not None:
            temp = list(self.memory)
            temp.append(int(new_value))
            self.memory = temp 
        return None

    @property
    def Comp_Output(self):
        return self.memory[-1]

    def LOOP_compute_until_output_or_stop(self, stop_at_each_output=True):
        ''' Drives execution of consecutive functions in codestring,
            until an OUTPUT or STOP condition is reached
            Option: Pause at each output OR Write outputs to memory until STOP
        '''
        self.FLAG_continue = True
        while True:  
            # ir:instruction_result
            step, ircode, irvalue = self.Compute_Instruction(self.curpos)
            if ircode == 'STOP_COMP':
                self.FLAG_continue = False
                print(f'Code stopped at position {self.curpos}')
                logging.info(f'Code stopped at position {self.curpos}')
                break
            elif ircode == 'OUTPUT':
                self.write_value_to_memory(irvalue)
                logging.debug(f'Code output {irvalue} at position {self.curpos}')
                self.curpos += step
                if stop_at_each_output is True: 
                    break
            elif ircode == 'NEXT_POS':
                self.curpos = irvalue if irvalue is not None else self.curpos + step
            else: 
                print(f'ircode {ircode} not recognized')
                raise ValueError
        return ircode

    def Compute_Instruction(self, position=None):    
        ''' Drives the interpretation & execution of Instruction
            at requested position (default Current Position
            Returns NEXTPOS, OUTPUT, or END ''' 
        # Find position and instruction value
        pos_instr = position if position is not None else self.curpos
        instr = self.sw[pos_instr]
        opcode, step, modes = self.Parse_Instr(instr)
        op_params = self.get_OpCode_Parameters(pos_instr, modes)
        # Call the correct OpCode function, passing 'params'
        ircode, irvalue = self.call_OpCode(opcode, params=op_params)
        return step, ircode, irvalue

    def Parse_Instr(self, instr):
        ''' Parse an instruction into it's parts: MMMOP  
            e.g., (Mode3,Mode2,Mode1,(OP,OP)) => 2 digit OpCode + 3 ParameterModes'''
        # Opcode stored in the two right-most digits
        opcode = int(str(instr)[-2::1])
        step = self.get_OpCode_Steps(opcode)
        # Modes: Read right-to-left, Leading zeroes are omitted in the Instruction
        modes = str(instr)[-3::-1].ljust(step-1, '0')
        return opcode, step, modes

    def get_OpCode_Parameters(self, pos_instr, modes):
        '''Interprets mode and collects Parameters for passing to OpCode'''
        op_params = []
        for i, mode in enumerate(modes[:]):
            pos_param = pos_instr + 1 + i
            op_params.append(self.Get_Param_by_Modes(pos_param, mode))
        return tuple(op_params)

    def Get_Param_by_Modes(self, Ppos, Mode): 
        ''' Returns the software position for OpCodes to reference
            0 = Position Mode - Refers to another position, index = value in current position
            1 = Immediate mode - Refers to current position
            2 = Relative mode - Refers to a position distant from reference position, value + relbase
            Note: Parameters that an instruction writes to will never be in Mode 1
        '''  
        instant = int(self.sw[Ppos])
        if Mode == '0':
            self.set_sw_pos(pos=instant)
            return instant  #int(self.sw[instant])
        elif Mode == '1': 
            return Ppos     #instant
        elif Mode == '2': 
            relative = instant+self.relbase
            self.set_sw_pos(pos=relative)
            return relative  #int(self.sw[relative]) 
        else: return "Mode not recognized"
        return None       

    _OPCODE_STEPS = dict(((1,4), (2,4), (3,2), (4,2), (5,3), (6,3), (7,4), (8,4), (9,2), (99,1)))
    @classmethod
    def get_OpCode_Steps(cls, op):
        return cls._OPCODE_STEPS.get(int(op), None)

    def call_OpCode(self, op, **kwargs):
        if   op == 1: return self.op_Add(**kwargs)
        elif op == 2: return self.op_Mult(**kwargs)
        elif op == 3: return self.op_Input(**kwargs)
        elif op == 4: return self.op_Output(**kwargs)
        elif op == 5: return self.op_JumpIfTrue(**kwargs)
        elif op == 6: return self.op_JumpIfFalse(**kwargs)
        elif op == 7: return self.op_LessThan(**kwargs)
        elif op == 8: return self.op_Equals(**kwargs)
        elif op == 9: return self.op_AdjRelBase(**kwargs)
        elif op == 99: return self.op_End()
        else: return self.bad_OpCode(op)
        return None

    def bad_OpCode(self, op):
        print(f'Bad Code: {op}')
        raise ValueError
        return None

    def op_End(self, **kwargs):       
        '''Opcode == 99:  # End program'''
        logging.info(f'99: End of Program at position {self.curpos}')
        logging.debug(f'SW Codestring at 99 stop: {self.sw}')
        return ('STOP_COMP', None)
    
    def op_Add(self, **kwargs):       
        ''' Opcode == 1:   # Addition
            Sets the indicated position to the sum of inputs '''
        [X, Y, Z] = kwargs.get('params', None)
        B, C, D = self.sw[X], self.sw[Y], Z
        result = int(B) + int(C)
        self.set_sw_pos(D, result)
        logging.debug(f'Add: Set position {D} to {result}')
        return ('NEXT_POS', None)       

    def op_Mult(self, **kwargs):      
        '''Opcode == 2:   # Multiplication'''
        [X, Y, Z] = kwargs.get('params', None)
        B, C, D = self.sw[X], self.sw[Y], Z
        result = int(B) * int(C)
        self.set_sw_pos(D, result)
        logging.debug(f'Mult: Set position {D} to {result}')
        return ('NEXT_POS', None)
    
    def op_Input(self, **kwargs):     
        '''#Opcode == 3:   # Request Input & Store at address'''
        (addr,) = kwargs.get('params', None)
        #addr = int(self.sw[Z])
        if self.MANUAL_INPUT is not True:
            inputvalue = self.input_value_generator()    
        else:
            inputvalue = int(input(f'Position {self.curpos}, Input integer: '))
        logging.debug(f'Set address {addr} to {inputvalue}')
        self.set_sw_pos(pos=addr, set_value=inputvalue)
        logging.info(f'Input: {inputvalue}')
        return ('NEXT_POS', None)
       
    def op_Output(self, **kwargs):    
        '''Opcode == 4:   # Output'''
        X = kwargs.get('params', None)[0]
        signal_out = int(self.sw[X])
        logging.debug(f'Output: Position {self.curpos}: {signal_out}')
        return ('OUTPUT', signal_out)
    
    def op_JumpIfTrue(self, **kwargs):     
        '''Opcode == 5:   #Jump-if-true'''
        [X, Y] = kwargs.get('params', None)
        B, C = int(self.sw[X]), int(self.sw[Y])
        if B != 0:
            jump2pos = C
            logging.debug(f'JT: B not 0, Going to position {jump2pos}')
            return ('NEXT_POS', jump2pos)
        else: 
            logging.debug(f'JT: B is 0, Going to next position')
            return ('NEXT_POS', None)
        
    def op_JumpIfFalse(self, **kwargs):     
        '''Opcode == 6:   #Jump-if-false'''
        [X, Y] = kwargs.get('params', None)
        B, C = int(self.sw[X]), int(self.sw[Y])
        if B == 0:
            jump2pos = C
            logging.debug(f'JF: B is 0, Going to position {jump2pos}')
            return ('NEXT_POS', jump2pos)
        else: 
            logging.debug(f'JF: B not 0, Going to next position')
            return ('NEXT_POS', None)   
       
    def op_LessThan(self, **kwargs):  
        ''' Opcode == 7:   # Less-Than'''
        [X, Y, Z] = kwargs.get('params', None)
        B, C, D = int(self.sw[X]), int(self.sw[Y]), Z
        result = 1 if B < C else 0
        self.set_sw_pos(D, result)
        logging.debug(f'LessThan: Setting position {D} to {result}')
        return ('NEXT_POS', None)
           
    def op_Equals(self, **kwargs):    
        '''Opcode == 8:   # Equals'''
        [X, Y, Z] = kwargs.get('params', None)
        B, C, D = int(self.sw[X]), int(self.sw[Y]), Z
        result = 1 if B == C else 0
        self.set_sw_pos(D, result)
        logging.debug(f'Equals: Setting position {D} to {result}')
        return ('NEXT_POS', None)     
           
    def op_AdjRelBase(self, **kwargs):    
        ''' Opcode == 9:   # Adjusts the relative base value'''
        X = kwargs['params'][0]
        delta = int(self.sw[X])
        if delta is not None:
            self.relbase += delta 
        logging.debug(f'New relative base: {self.relbase}')
        return ('NEXT_POS', None)

    def input_value_generator(cls):
        # Instance should define it's own input value generator function
        logging.info('Default input generator value was used')
        return 0

    @staticmethod
    def Find_Dict_Max_Value(dict1):
        return max(dict1.items(), key=lambda x: x[1])  
# End Class Comp_Intcode


def main():  
    """ Basic test: What is the diagnostic code for system ID 5? [INPUT = 5]
    Your puzzle answer was 11460760 at Pos 676
    """
    #sw_test = "X:\Python\PyChallenge\AOC2019_05.txt"
    #sw_test = "AOC2019_05.txt"

    sw_test = "AOC2019_09Test.txt"  # Quine

    comp1 = Comp_Intcode(sw_test)
    while True:
        comp1.LOOP_compute_until_output_or_stop(stop_at_each_output = False)
        loop_again = input("Loop again?")
        if loop_again.lower() != 'y':
            break

    print('End of Main', comp1._memory)
    logging.info('End of Main', comp1._memory)


if __name__ == '__main__':
    main()

