from typing import List, Tuple
from collections import deque, namedtuple, defaultdict

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


class IntcodeProgram:

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

        program = self.program

        while True:
        
            opcode, modes = instruction_to_opcodemode(program[self.ptr])
            # print("program :", program.values())
            # print("opcode : ",Opcode(opcode), "modes: ", modes, "relative_base :", self.relative_base, "ptr : ", self.ptr)
            # print("outputs :", outputs)
            
            if program[self.ptr] == 99:
                raise EOFError("Program end")

            elif Opcode(opcode) == Opcode.plus: # +
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
                self.ptr += 2
                return value
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



Panel = namedtuple("Panel", ["x", "y"])

class Direction(Enum):

    up = 0
    left = 1
    bottom = 2
    right = 3

def turn(direction: Direction, turn: int) -> Direction:
    # 0 left, 1 right turn
    turn = turn * 2 - 1
    # -1 left, 1 right
    return Direction((direction.value - turn) % 4)

def move(pos: Panel, direction: Direction) -> Panel:
    if direction == Direction.up:
        new = Panel(pos.x, pos.y+1)
    elif direction == Direction.left:
        new = Panel(pos.x-1, pos.y)
    elif direction == Direction.bottom:
        new = Panel(pos.x, pos.y-1)
    elif direction == Direction.right:
        new = Panel(pos.x+1, pos.y)
    return new

def run_robot(program: Program, start_color: int=0) -> List[Panel]:

    panels = defaultdict(int)
    painted = set()
    robot = IntcodeProgram(program)

    pos = Panel(0,0)
    direction = Direction.up

    panels[pos] = start_color

    try:
        while True:
            color = panels[pos]
            to_paint = robot.run(color)
            to_move = robot.run()

            panels[pos] = to_paint
            painted.add(pos)
            direction = turn(direction, to_move)
            pos = move(pos, direction)
    except EOFError:
        print("program terminated with {} painted cells".format(len(painted)))

    return panels

with open('input') as f:
    program = [int(i) for i in f.readline().strip().split(',')]

# _ = run_robot(program)

panels = run_robot(program, 1)

painted_panels = [panel for panel in panels if panels[panel] == 1]

def show(panels: List[Panel], symbol: str='*') -> str:
    x_max = max([panel.x for panel in panels])
    x_min = min([panel.x for panel in panels])
    x_range = x_max-x_min

    y_max = max([panel.y for panel in panels])
    y_min = min([panel.y for panel in panels])
    y_range = y_max-y_min

    output = []
    for y in range(y_max, y_min-1, -1):
        line = []
        for x in range(x_min, x_max+1):
            if Panel(x, y) in panels:
                line.append(symbol)
            else:
                line.append(' ')
        output.append(''.join(line))
    return '\n'.join(output)


print(show(painted_panels))