from typing import List, Tuple
from collections import deque

from enum import Enum


Program = List[int]


class Opcode(Enum):

    plus = 1
    multiply = 2
    input_value = 3
    output_value = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    relative_base_offset = 9

class ParamMode(Enum):
    position = 0
    immediate = 1
    relative = 2


def instruction_to_opcodemode(instruction: int) -> Tuple[int]:
    digits = [i for i in str(instruction).zfill(5)]
    opcode = int(''.join(digits[3:]))
    modes = [int(i) for i in reversed(digits[0:3])]
    return opcode, modes


class Amplifier:

    def __init__(self, program: Program, phase: int=None) -> None:
        self.program = dict(enumerate(program[:]))
        self.ptr = 0
        self.relative_base = 0

        if phase is not None:
            self.inputs = deque([phase])
        else:
            self.inputs = deque([])

    def get_addr(self, ptr: int, mode: int) -> int:

        if ParamMode(mode) == ParamMode.position:
            addr = self.program[ptr]
        elif ParamMode(mode) == ParamMode.immediate:
            addr = ptr
        elif ParamMode(mode) == ParamMode.relative:
            addr = self.program[ptr] + self.relative_base
        else:
            raise ValueError("Unknown mode {}".format(mode))

        if addr < 0:
                raise ValueError("Invalid Memory Access : {}".format(addr))
        return addr

    def get_value(self, ptr: int, mode: int) -> int:

        addr = self.get_addr(ptr, mode)
        return self.program.get(addr, 0)

    def get_3ptr(self, modes):
        value1 = self.get_value(self.ptr+1, modes[0])
        value2 = self.get_value(self.ptr+2, modes[1])
        addr3 = self.get_addr(self.ptr+3, modes[2])
        return value1, value2, addr3

    def get_2ptr(self, modes):
        value1 = self.get_value(self.ptr+1, modes[0])
        value2 = self.get_value(self.ptr+2, modes[1])
        return value1, value2

    def run(self, input_value: int=None) -> int:
        if input_value is not None:
            self.inputs.append(input_value)

        outputs = []
        program = self.program

        while program[self.ptr] != 99:

            opcode, modes = instruction_to_opcodemode(program[self.ptr])
            # print("program :", program.values())
            # print("opcode : ",Opcode(opcode), "modes: ", modes, "relative_base :", self.relative_base, "ptr : ", self.ptr)
            # print("outputs :", outputs)

            if Opcode(opcode) == Opcode.plus: # +
                value1, value2, addr3 = self.get_3ptr(modes)
                program[addr3] = value1 + value2
                # print("value1: ", value1, "value2: ", value2, "value3: ", value1 + value2, "addr3: ", addr3)
                self.ptr += 4
            elif Opcode(opcode) == Opcode.multiply: # *
                value1, value2, addr3 = self.get_3ptr(modes)
                # print("value1: ", value1, "value2: ", value2, "value3: ", value1 * value2, "addr3: ", addr3)
                program[addr3] = value1 * value2
                self.ptr += 4
            elif Opcode(opcode) == Opcode.input_value: # input
                addr = self.get_addr(self.ptr+1, modes[0])
                try:
                    program[addr] = self.inputs.pop()
                except IndexError:
                    print("No more inputs")
                    program[addr] = 0
                self.ptr += 2
            elif Opcode(opcode) == Opcode.output_value: # output
                # print("instruction: ",program[self.ptr:self.ptr+2])
                value = self.get_value(self.ptr+1, modes[0])
                # print("value: ", value)
                outputs.append(value)
                self.ptr += 2
            elif Opcode(opcode) == Opcode.jump_if_true: # jump-if-true
                value1, value2 = self.get_2ptr(modes)
                if value1 != 0:
                    self.ptr = value2
                else:
                    self.ptr += 3
            elif Opcode(opcode) == Opcode.jump_if_false: # jump-if-false
                value1, value2 = self.get_2ptr(modes)
                if value1 == 0:
                    self.ptr = value2
                else:
                    self.ptr += 3
            elif Opcode(opcode) == Opcode.less_than: # less than
                value1, value2, addr3 = self.get_3ptr(modes)
                if value1 < value2:
                    program[addr3] = 1
                else:
                    program[addr3] = 0     
                self.ptr += 4
            elif Opcode(opcode) == Opcode.equals: # equals
                value1, value2, addr3 = self.get_3ptr(modes)
                if value1 == value2:
                    program[addr3] = 1
                else:
                    program[addr3] = 0  
                self.ptr += 4
            elif Opcode(opcode) == Opcode.relative_base_offset:
                value1 = self.get_value(self.ptr+1, modes[0])
                self.relative_base += value1
                self.ptr += 2
            else:
                raise ValueError("Wrong opcode {}".format(opcode))
        return outputs

PROGRAM = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
assert Amplifier(PROGRAM, None).run() == PROGRAM

PROGRAM = [1102,34915192,34915192,7,4,7,99,0]
assert len(str(Amplifier(PROGRAM, None).run()[0])) == 16

PROGRAM = [104,1125899906842624,99]
assert Amplifier(PROGRAM, None).run()[0] == PROGRAM[1]

with open('input') as f:
    program = [int(code) for code in f.readline().strip().split(',')]

print(Amplifier(program, 1).run())
print(Amplifier(program, 2).run())