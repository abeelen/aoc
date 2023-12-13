from intcode import IntcodeProgram
from collections import namedtuple
from typing import List, Dict
from enum import Enum


Position = namedtuple("Position", ["x", "y"])
class Status(Enum):
    """    
    0: The repair droid hit a wall. Its position has not changed.
    1: The repair droid has moved one step in the requested direction.
    2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
    """
    wall = 0
    moved = 1
    oxygen = 2


def parse_screen(screen: List[str]) -> Dict[Position, str]:
    n_y = len(screen)
    n_x = len(screen[0])

def draw_image(program: List[int]) -> List[str]:
    camera = IntcodeProgram(program)
    pixels = []
    try:
        while True:
            pixels.append(chr(camera.run()))
    except StopIteration:
        pass

    return ''.join(pixels).split('\n')

with open('input') as f:
    program = [int(i) for i in f.readline().strip().split(',')]


screen = draw_image(program)