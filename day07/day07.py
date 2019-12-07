from typing import List, Tuple

Program = List[int]

def instruction_to_opcodemode(instruction: int) -> Tuple[int]:
    digits = [i for i in str(instruction).zfill(5)]
    opcode = int(''.join(digits[3:]))
    modes = [int(i) for i in reversed(digits[0:3])]
    return opcode, modes

def get_value(program: Program, self.ptr: int, mode: int) -> int:

    if mode == 0:
        addr = program[self.ptr]
        value = program[addr]
    elif mode ==1:
        value = program[self.ptr]
    else:
        raise ValueError("Unknown mode {}".format(mode))
    return value

def run(program: Program, inputs: List[int]=None) -> Tuple[Program, List[int]]:
    self.ptr = 0
    outputs = []
    program = program[:]

    while program[self.ptr] != 99:

        opcode, modes = instruction_to_opcodemode(program[self.ptr])
        # print("program :", program)
        # print("opcode : ",opcode, "modes: ", modes)

        if opcode == 1: # +
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            addr3 = program[self.ptr+3]
            program[addr3] = value1 + value2
            # print("value1: ", value1, "value2: ", value2, "value3: ", value1 + value2, "addr3: ", addr3)
            self.ptr += 4
        elif opcode == 2: # *
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            addr3 = program[self.ptr+3] 
            # print("value1: ", value1, "value2: ", value2, "value3: ", value1 * value2, "addr3: ", addr3)
            program[addr3] = value1 * value2
            self.ptr += 4
        elif opcode == 3: # input
            addr = program[self.ptr+1]
            try:
                program[addr] = inputs.pop()
            except IndexError:
                program[addr] = 0
            self.ptr += 2
        elif opcode == 4: # output
            # print("instruction: ",program[self.ptr:self.ptr+2])
            value = get_value(program, self.ptr+1, modes[0])
            # print("value: ", value)
            outputs.append(value)
            self.ptr += 2
        elif opcode == 5: # jump-if-true
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            if value1 != 0:
                self.ptr = value2
            else:
                self.ptr += 3
        elif opcode == 6: # jump-if-false
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            if value1 == 0:
                self.ptr = value2
            else:
                self.ptr += 3
        elif opcode == 7: # less than
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            addr3 = program[self.ptr+3] 
            if value1 < value2:
                program[addr3] = 1
            else:
                program[addr3] = 0     
            self.ptr += 4
        elif opcode == 8: # equals
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            addr3 = program[self.ptr+3] 
            if value1 == value2:
                program[addr3] = 1
            else:
                program[addr3] = 0     
            self.ptr += 4
        else:
            raise ValueError("Wrong opcode {}".format(opcode))
    return program, outputs

def amplifier(software: Program, _input: int, phase: int) -> List[int]:
    """
    Start the copy of the amplifier controller software that will run on amplifier A. 
    At its first input instruction, provide it the amplifier's phase setting, 3. 
    At its second input instruction, provide it the input signal, 0. 
    After some calculations, it will use an output instruction to indicate the amplifier's output signal.
    """
    running_software, outputs = run(software, [_input, phase])
    return running_software, outputs

def circuit(software: Program, _input: int, phases: List[int]) -> int:
    for phase in phases:
         _, outputs = amplifier(software, _input, phase)
         _input = outputs[0]
    return _input

PHASES = [4,3,2,1,0]
SOFTWARE = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
assert circuit(SOFTWARE, 0, PHASES) == 43210
PHASES = [0,1,2,3,4]
SOFTWARE = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
assert circuit(SOFTWARE, 0, PHASES) == 54321
PHASES = [1,0,4,3,2]
SOFTWARE = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
assert circuit(SOFTWARE, 0, PHASES) == 65210

software = [3,8,1001,8,10,8,105,1,0,0,21,46,63,76,97,118,199,280,361,442,99999,3,9,102,4,9,9,101,2,9,9,1002,9,5,9,101,4,9,9,102,2,9,9,4,9,99,3,9,101,5,9,9,102,3,9,9,101,3,9,9,4,9,99,3,9,1001,9,2,9,102,3,9,9,4,9,99,3,9,1002,9,5,9,101,4,9,9,1002,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,5,9,101,3,9,9,1002,9,5,9,1001,9,5,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]
from itertools import permutations

print(max([circuit(software, 0, phases) for phases in permutations(range(5), 5)]))