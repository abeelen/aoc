from typing import List, Tuple, Dict
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

class IntcodeProgram():

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
                raise StopIteration("Program done")

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

with open('input') as f:
    program = [int(i) for i in f.readline().strip().split(',')]

class TileId(Enum):
    empty = 0
    wall = 1
    block = 2
    paddle = 3
    ball = 4

"""   
    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.
"""

Tile = namedtuple("tile", ["x", "y"])

def draw_tiles(program: Program) -> Dict[Tile, TileId]:
    arcade = IntcodeProgram(program)
    screen: Dict[Tile, TileI] = {}

    try:
        while True:
            x, y, tile_id = arcade.run(), arcade.run(), arcade.run()
            screen[Tile(x, y)] = TileId(tile_id)
    except StopIteration:
        return screen


screen = draw_tiles(program)
# print(sum([True for tile_id in screen.values() if tile_id == TileId.block]))

# part 2
def draw_tile(tile_id: TileId) -> str:
    if tile_id == TileId.empty:
        return ' '
    elif tile_id == TileId.paddle:
        return '_'
    elif tile_id == TileId.wall:
        return '#'
    elif tile_id == TileId.ball:
        return 'o'           
    elif tile_id == TileId.block:
        return 'x'
    else:
        raise ValueError("Unknown tile : {}".format(tile_id))

def draw(screen: Dict[Tile, TileId]) -> None:
    x_max = max([tile.x for tile in screen])
    x_min = min([tile.x for tile in screen])

    y_max = max([tile.y for tile in screen])
    y_min = min([tile.y for tile in screen])

    lines = []
    for y in range(y_min, y_max+1):
        line = [draw_tile(screen.get(Tile(x, y), TileId.empty)) for x in range(x_min, x_max+1)]
        lines.append("".join(line))
    print("\n".join(lines))

class Joystick(Enum):
    neutral = 0
    left = -1
    right = 1


def play_game(program: Program) -> int:
    program[0] = 2
    score = 0
    input_value = None

    arcade = IntcodeProgram(program)
    screen: Dict[Tile, TileId] = {}

    paddle_tile = None
    ball_tile = None

    try:
        while True:
            x, y, tile_id = arcade.run(input_value), arcade.run(), arcade.run()
            if x == -1 and y == 0:
                score = tile_id
            else:
                tile_id = TileId(tile_id)
                tile = Tile(x, y)
                screen[tile] = tile_id

                # Track position of ball and paddle
                if tile_id == TileId.paddle:
                    paddle_tile = tile
                elif tile_id == TileId.ball:
                    ball_tile = tile
            
            if paddle_tile and ball_tile:
                if paddle_tile.x < ball_tile.x:
                    input_value = Joystick.right.value
                elif paddle_tile.x > ball_tile.x:
                    input_value = Joystick.left.value
                elif paddle_tile.x == ball_tile.x:
                    input_value = Joystick.neutral.value                   


            draw(screen)
            print(score)
    except StopIteration:
        return score


play_game(program)