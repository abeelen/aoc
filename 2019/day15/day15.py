from typing import List, Tuple, Dict

from intcode import IntcodeProgram, Program
from collections import namedtuple, deque

from enum import Enum
import random
from copy import deepcopy

class Direction(Enum):
    north = 1
    south = 2
    west = 3
    east = 4

class Status(Enum):
    """    
    0: The repair droid hit a wall. Its position has not changed.
    1: The repair droid has moved one step in the requested direction.
    2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
    """
    wall = 0
    moved = 1
    oxygen = 2



with open('input') as f:
    program = [int(i) for i in f.readline().strip().split(',')]


Position = namedtuple("Position", ["x", "y"])

def update_position(pos: Position, direction: Direction) -> Position:

    x, y = pos
    if direction == Direction.north:
        y += 1
    elif direction == Direction.south:
        y -= 1
    elif direction == Direction.east:
        x += 1
    elif direction == Direction.west:
        x -= 1
    else:
        raise ValueError("Wrong direction : {}".format(direction))

    return Position(x, y)

def update_direction(direction: Direction) -> Direction:

    return Direction(random.randint(1, 4))

    #if direction == Direction.north:
    #    return Direction.west if random.random() > 0.5 else Direction.south
    #elif direction == Direction.west:
    #    return Direction.south if random.random() > 0.5 else Direction.east
    #elif direction == Direction.south:
    #    return Direction.east if random.random() > 0.5 else Direction.north
    #elif direction == Direction.east:
    #    return Direction.north if random.random() > 0.5 else Direction.west
    #else:
    #    raise ValueError("Unknown direction")

def draw_pixel(status: Status) -> str:
    if status == Status.wall:
        return "#"
    elif status == Status.moved:
        return "."
    elif status == Status.oxygen:
        return "*"
    else:
        return " "

def draw_map(grid: List[Position], pos: Position) -> str:

    x_max = max([wall.x for wall in grid])
    x_min = min([wall.x for wall in grid])

    y_max = max([wall.y for wall in grid])
    y_min = min([wall.y for wall in grid])

    lines = []
    for y in range(y_min, y_max+1):
        line = [draw_pixel(grid.get(Position(x, y), None)) for x in range(x_min, x_max+1)]
        lines.append("".join(line))
    print("\n".join(lines))

def random_mouse(program: Program) -> Dict[Position, Status]:

    droid = IntcodeProgram(program)

    pos = Position(0,0)
    direction = Direction.north
    status = Status.moved
    grid = {}
    iter = 0
    while status != Status.oxygen:
        status = Status(droid.run(direction.value))
        iter+=1
        if not iter % 5000:
            draw_map(grid, pos)

        # print("pos: ", pos)
        # print("direction: ", direction)
        # print("status: ", status)
        if status == Status.moved:
            pos = update_position(pos, direction)
            grid[pos] = Status.moved
            # if random.random() < 0.8:
            direction = update_direction(direction)
        elif status == Status.wall:
            grid[update_position(pos, direction)] = Status.wall
            direction = update_direction(direction)
        elif status == Status.oxygen:
            grid[update_position(pos, direction)] = Status.oxygen
            return grid


def breadth_first_search(program: Program, draw=False) -> Tuple[IntcodeProgram, int]:

    droid = IntcodeProgram(program)
    pos = Position(0,0)
    direction = Direction.north
    status = Status.moved
    dist = 0
    grid = {pos: status}

    queue = deque([])
    for direction in range(1,5):
        queue.append((deepcopy(droid), pos, Direction(direction), dist+1))

    iter = 0

    while(queue):
        # iter+=1
        # if not iter % 10:
        if draw and grid:
            draw_map(grid, pos)
        droid, pos, direction, dist = queue.popleft()
        status = Status(droid.run(direction.value))
        if status == Status.oxygen:
            grid[update_position(pos, direction)] = Status.oxygen
            draw_map(grid, pos)
            return droid, dist
        elif status == Status.wall:
            grid[update_position(pos, direction)] = Status.wall
        elif status == Status.moved:
            pos = update_position(pos, direction)
            if pos not in grid:
                grid[pos] = Status.moved
                for direction in range(1,5):
                    queue.append((deepcopy(droid), pos, Direction(direction), dist+1))



random.seed(42)
# grid = random_mouse(program)
droid, dist = breadth_first_search(program)
print(dist)

def breadth_first_fill(droid: IntcodeProgram, draw=False) -> int:

    # Start from the oxygen
    pos = Position(0,0)
    direction = Direction.north
    status = Status.moved
    num_visited = -1
    grid = {pos: status}

    queue = deque([])
    for direction in range(1,5):
        queue.append((deepcopy(droid), pos, Direction(direction), num_visited+1))

    while(queue):
        if draw and grid:
            draw_map(grid, pos)
        droid, pos, direction, num_visited = queue.popleft()
        status = Status(droid.run(direction.value))
        if status == Status.wall:
            grid[update_position(pos, direction)] = Status.wall
        elif status == Status.moved:
            pos = update_position(pos, direction)
            if pos not in grid:
                grid[pos] = Status.oxygen
                for direction in range(1,5):
                    queue.append((deepcopy(droid), pos, Direction(direction), num_visited+1))

    draw_map(grid, pos)
    return num_visited

print(breadth_first_fill(droid))