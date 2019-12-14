from typing import List, Tuple, Dict
from collections import namedtuple
from operator import itemgetter

Location = namedtuple('Location', ['X', 'Y'])

def parse_map(asteroid_map: List[List[str]]) -> List[Location]:
    locations = []
    for j, line in enumerate(asteroid_map):
        for i, pos in enumerate(line):
            if pos == "#":
                locations.append(Location(i,j))
    return locations


from math import atan2

def detection(locations: List[Location]) -> Dict[Location, int]:
    direct_detections = []
    for asteroid in locations:
        neighbour = []
        for target in locations:
            if target != asteroid:
                neighbour.append(atan2(target.Y-asteroid.Y, target.X-asteroid.X))
        neighbour = set(neighbour)
        direct_detections.append((asteroid, len(neighbour)))
    return dict(direct_detections)

def best_location(detections: Dict[Location, int]) -> Location:
    # return max(detections.keys(), key=lambda k: detections[k])
    return max(detections.items(), key=itemgetter(1))

INPUT=""".#..#
.....
#####
....#
...##
"""
assert best_location(detection(parse_map(INPUT.split('\n')))) == (Location(3,4), 8)

INPUT="""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
assert best_location(detection(parse_map(INPUT.split('\n')))) == (Location(5,8), 33)

INPUT="""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
assert best_location(detection(parse_map(INPUT.split('\n')))) == (Location(1,2), 35)

INPUT=""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
assert best_location(detection(parse_map(INPUT.split('\n')))) == (Location(6,3), 41)

INPUT=""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
assert best_location(detection(parse_map(INPUT.split('\n')))) == (Location(11,13), 210)

inputs = """##.##..#.####...#.#.####
##.###..##.#######..##..
..######.###.#.##.######
.#######.####.##.#.###.#
..#...##.#.....#####..##
#..###.#...#..###.#..#..
###..#.##.####.#..##..##
.##.##....###.#..#....#.
########..#####..#######
##..#..##.#..##.#.#.#..#
##.#.##.######.#####....
###.##...#.##...#.######
###...##.####..##..#####
##.#...#.#.....######.##
.#...####..####.##...##.
#.#########..###..#.####
#.##..###.#.######.#####
##..##.##...####.#...##.
###...###.##.####.#.##..
####.#.....###..#.####.#
##.####..##.#.##..##.#.#
#####..#...####..##..#.#
.##.##.##...###.##...###
..###.########.#.###..#.
"""

print(best_location(detection(parse_map(inputs.split('\n')))))
