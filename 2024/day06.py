from collections import namedtuple
from itertools import cycle
from typing import List, Tuple
from tqdm import tqdm

RAW_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

Pos = namedtuple("pos", ["x", "y"])

directions = cycle([(0, 1), (-1, 0), (0, -1), (1, 0)])


def parse_input(raw_input: str) -> Tuple[Pos, Pos, List[Pos]]:
    lines = raw_input.split("\n")
    obstacles = []
    for j, line in enumerate(lines):
        for i in range(len(line)):
            if line[i] == "#":
                obstacles.append(Pos(i, j))
            elif line[i] == "^":
                start = Pos(i, j)
                direction = (0, -1)

    return start, direction, obstacles


def init_directions(direction):
    # initialize directions :
    while next(directions) != direction:
        pass


def guard_route(start: Pos, start_direction: Pos, obstacles: List[Pos]) -> int:
    pos = start
    direction = start_direction
    visited = set([start])
    loop = set([start, direction])
    xmin = ymin = 0
    xmax = max([pos.x for pos in obstacles])
    ymax = max([pos.y for pos in obstacles])

    init_directions(direction)

    while pos.x > xmin and pos.y > ymin and pos.x < xmax and pos.y < ymax:
        # print(pos, direction, visited)
        nextpos = Pos(pos.x + direction[0], pos.y + direction[1])
        if nextpos in obstacles:
            direction = next(directions)
        else:
            pos = nextpos
            visited.add(pos)
        if (pos, direction) in loop:
            raise ValueError("In a loop")
        loop.add((pos, direction))

    return visited


def guard_in_a_loop(start: Pos, direction: Pos, obstacles: List[Pos]) -> int:
    normal_route = guard_route(start, direction, obstacles)
    # Brute force approach...
    possible_position = list(normal_route - set([start]))

    loop_position = set()
    for new_obstacle in tqdm(possible_position):
        try:
            guard_route(start, direction, obstacles + [new_obstacle])
        except ValueError:
            loop_position.add(new_obstacle)
    return loop_position


start, direction, obstacles = parse_input(RAW_INPUT)
assert len(guard_route(start, direction, obstacles)) == 41
assert len(guard_in_a_loop(start, direction, obstacles)) == 6

with open("day06.txt", "r") as f:
    raw_input = f.read().strip()

start, direction, obstacles = parse_input(raw_input)

print(len(guard_route(start, direction, obstacles)))
print(len(guard_in_a_loop(start, direction, obstacles)))
