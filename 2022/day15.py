from dataclasses import dataclass
import re
from typing import Tuple, Dict, List
from functools import cached_property

@dataclass
class Point:
    x: int
    y: int

    def manhattan_distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

@dataclass
class Sensor:
    pos: Point
    beacon: Point

    @cached_property
    def distance_to_beacon(self) -> int:
        return self.pos.manhattan_distance(self.beacon)

Problem = List[Sensor]
World = Dict[Tuple[int, int], str]

def parse_problem(raw: str)-> Problem:
    pattern = "Sensor at x=([+-]?\d+), y=([+-]?\d+): closest beacon is at x=([+-]?\d+), y=([+-]?\d+)"
    return [Sensor(Point(int(line[0]), int(line[1])), Point(int(line[2]), int(line[3]))) for line in re.findall(pattern, raw)]

def print_world(world: World) -> None:
    min_x = min(item[0] for item in world.keys())
    max_x = max(item[0] for item in world.keys())
    min_y = min(item[1] for item in world.keys())
    max_y = max(item[1] for item in world.keys())

    repr = []
    for y in range(min_y, max_y):
        row = "" 
        for x in range(min_x, max_x):
            row += world.get((x, y), '.')
        repr.append(row)
    return '\n'.join(repr)

def make_world(problem: Problem) -> Problem:
    world = {}
    for sensor in problem:
        world[(sensor.pos.x, sensor.pos.y)] = 'S'
        world[(sensor.beacon.x, sensor.beacon.y)] = 'B'

    # No distress signal : 
    for sensor in problem:
        dist = sensor.distance_to_beacon
        x, y = sensor.pos.x, sensor.pos.y
        for i in range(0, dist+1):
            for j in range(0, dist+1-i):
                for pos in [(x + i, y + j), (x - i, y + j), (x + i, y - j), (x -i, y - j)]:
                    if pos not in world:
                        world[pos] = "#"

    return world

def counting_no_beacon_brute(world: World, row=10) -> int:
    return len([item for item in world.keys() if item[1] == row and world[item] == '#'])

def counting_no_beacon(problem: Problem, row=10) -> int:

    line = set()
    beacon_and_sensor_on_row = set([item.pos.x for item in problem if item.pos.y == row] + [item.beacon.x for item in problem if item.beacon.y == row])
    for item in problem:
        projected_distance  = abs(item.pos.y - row)
        if projected_distance > item.distance_to_beacon:
            continue
        for i in range(0, item.distance_to_beacon - projected_distance + 1):
            x_pos = [item.pos.x + i, item.pos.x - i]
            for pos in x_pos:
                if pos not in beacon_and_sensor_on_row:
                    line.add(pos)
            
    return len(line)

def find_missing_beacon(problem: Problem, at_most: int= 20) -> Tuple[int, int]:
    # find the only empty solution within [0, 4_000_000]
    # the beacon must be at +1 from a sensor
    # Test for the annulus around sensors against all other sensors
    for beacon in problem:
        dist = beacon.distance_to_beacon
        for dx in range(dist+2):
            dy = dist - dx + 1
            for _dx, _dy in [( +dx, +dy), (-dx, +dy), (+dx, -dy), (-dx, -dy)]:
                pos = [beacon.pos.x + _dx, beacon.pos.y + _dy]
                if pos[0] < 0 or pos[1] < 0 or pos[0] > at_most or pos[1] > at_most:
                    continue
                if all(item.pos.manhattan_distance(Point(*pos)) > item.distance_to_beacon for item in problem):
                    return pos
        
def tuning_frequency(pos: Tuple[int, int]) -> int:
    return pos[0] * 4_000_000 + pos[1]

RAW="""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

assert counting_no_beacon_brute(make_world(parse_problem(RAW))) == 26
assert counting_no_beacon(parse_problem(RAW)) == 26

with open('day15.txt') as f:
    raw = f.read()

print(counting_no_beacon(parse_problem(raw), row=2_000_000))

assert tuning_frequency(find_missing_beacon(parse_problem(RAW))) == 56000011

print(tuning_frequency(find_missing_beacon(parse_problem(raw), at_most=4_000_000)))