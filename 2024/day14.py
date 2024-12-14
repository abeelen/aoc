import re
from collections import namedtuple
from functools import reduce
from itertools import product
from operator import mul
from typing import List

RAW_INPUT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

WIDTH = 11
HEIGHT = 7

Pos = namedtuple("Pos", ["x", "y"])
Vel = namedtuple("Vel", ["dx", "dy"])
Robot = namedtuple("Robot", ["pos", "vel"])


def parse_input(raw_input: str) -> List[Robot]:
    robots = []
    for item in re.finditer(r"p=(\d+,\d+) v=(-?\d+,-?\d+)", raw_input):
        x, y = map(int, item.group(1).split(","))
        dx, dy = map(int, item.group(2).split(","))
        robots.append(Robot(Pos(x, y), Vel(dx, dy)))
    return robots


def move_robot(robot: Robot, time: int, width: int, height: int) -> Robot:
    new_x = (robot.pos.x + robot.vel.dx * time) % width
    new_y = (robot.pos.y + robot.vel.dy * time) % height
    return Robot(Pos(new_x, new_y), robot.vel)


def move_robots(robots: List[Robot], time: int, width: int, height: int) -> List[Robot]:
    return [move_robot(robot, time, width, height) for robot in robots]


def safety_factor(robots: List[Robot], time: int, width: int, height: int) -> int:
    robots = move_robots(robots, time, width, height)
    x_quadrants = [[0, width // 2], [width // 2 + 1, width]]
    y_quadrants = [[0, height // 2], [height // 2 + 1, height]]
    robots_per_quadrant = []
    for (x_start, x_end), (y_start, y_end) in product(x_quadrants, y_quadrants):
        n_robots = sum(x_start <= robot.pos.x < x_end and y_start <= robot.pos.y < y_end for robot in robots)
        robots_per_quadrant.append(n_robots)

    return reduce(mul, robots_per_quadrant)


def draw_robots(robots: List[Robot], width: int, height: int) -> str:
    grid = [["." for _ in range(width)] for _ in range(height)]
    for robot in robots:
        grid[robot.pos.y][robot.pos.x] = "#"
    return "\n".join("".join(row) for row in grid)


assert move_robot(Robot(Pos(2, 4), Vel(2, -3)), 1, 11, 7) == Robot(Pos(4, 1), Vel(2, -3))
assert move_robot(Robot(Pos(2, 4), Vel(2, -3)), 2, 11, 7) == Robot(Pos(6, 5), Vel(2, -3))
assert move_robot(Robot(Pos(2, 4), Vel(2, -3)), 5, 11, 7) == Robot(Pos(1, 3), Vel(2, -3))


ROBOTS = parse_input(RAW_INPUT)
assert safety_factor(ROBOTS, 100, WIDTH, HEIGHT) == 12

with open("day14.txt") as f:
    raw_input = f.read().strip()

robots = parse_input(raw_input)
print(safety_factor(robots, 100, 101, 103))


# Part 2
# How to define  a x-mas tree ?
# symetry with vertical axis ?


def is_xmas_tree2(robots: List[Robot], width: int, height: int) -> bool:
    # Find the base of the tree
    image = draw_robots(robots, width, height)
    if "########" in image:
        return True
    return False


from tqdm import trange


def find_xmas_tree(robots: List[Robot], width: int, height: int) -> int:
    for i in trange(10_000):
        if is_xmas_tree2(robots, width, height):
            break
        robots = move_robots(robots, 1, width, height)

    print(draw_robots(robots, width, height))
    print(i)


find_xmas_tree(robots, 101, 103)
