from typing import List, Tuple
from collections import deque
Program = List[int]

def instruction_to_opcodemode(instruction: int) -> Tuple[int]:
    digits = [i for i in str(instruction).zfill(5)]
    opcode = int(''.join(digits[3:]))
    modes = [int(i) for i in reversed(digits[0:3])]
    return opcode, modes

def get_value(program: Program, ptr: int, mode: int) -> int:

    if mode == 0:
        addr = program[ptr]
        value = program[addr]
    elif mode ==1:
        value = program[ptr]
    else:
        raise ValueError("Unknown mode {}".format(mode))
    return value

class Amplifier:

    def __init__(self, program: Program, phase: int) -> None:
        self.program = program[:]
        self.ptr = 0
        self.inputs = deque([phase])

    def run(self, input_value: int=None) -> int:
        self.inputs.append(input_value)

        program = self.program

        while True:

            opcode, modes = instruction_to_opcodemode(program[self.ptr])

            if opcode == 99:
                return None
            elif opcode == 1: # +
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
                program[addr] = self.inputs.popleft()

                self.ptr += 2
            elif opcode == 4: # output
                # print("instruction: ",program[self.ptr:self.ptr+2])
                value = get_value(program, self.ptr+1, modes[0])
                # print("value: ", value)
                self.ptr += 2
                return value
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


def feedback_circuit(software: Program, phases: List[int]) -> int:
    amplifiers = [Amplifier(software, phase) for phase in phases]

    n = len(amplifiers)
    finished = [0] * n

    last_output = 0 # First input
    aid = 0

    while sum(finished) < n:
        output = amplifiers[aid].run(last_output)
        if output is None:
            finished[aid] = 1
        else:
            last_output = output

        aid = (aid + 1) % n
    return last_output

SOFTWARE = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
PHASES = [9,8,7,6,5]
assert feedback_circuit(SOFTWARE, PHASES) == 139629729

SOFTWARE = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
PHASES = [9,7,8,5,6]
assert feedback_circuit(SOFTWARE, PHASES) == 18216


software = [3,8,1001,8,10,8,105,1,0,0,21,46,63,76,97,118,199,280,361,442,99999,3,9,102,4,9,9,101,2,9,9,1002,9,5,9,101,4,9,9,102,2,9,9,4,9,99,3,9,101,5,9,9,102,3,9,9,101,3,9,9,4,9,99,3,9,1001,9,2,9,102,3,9,9,4,9,99,3,9,1002,9,5,9,101,4,9,9,1002,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,5,9,101,3,9,9,1002,9,5,9,1001,9,5,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]
from itertools import permutations
print(max([feedback_circuit(software, phases) for phases in permutations(range(5, 10), 5)]))