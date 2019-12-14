from typing import List, Tuple, Dict, Iterator
from collections import namedtuple
from operator import itemgetter
from collections import defaultdict

Location = namedtuple('Location', ['X', 'Y'])

def parse_map(asteroid_map: List[List[str]]) -> List[Location]:
    locations = []
    for j, line in enumerate(asteroid_map):
        for i, pos in enumerate(line):
            if pos == "#":
                locations.append(Location(i,j))
    return locations


from math import atan2, pi

def line_of_sight(locations: List[Location], station: Location) -> Dict[Location, float]:
    line_of_sights = defaultdict(list)
    for asteroid in locations:
        if asteroid != station:
            angle = atan2(asteroid.Y-station.Y, asteroid.X-station.X)
            #atan2 goes from -pi to pi, we want to count from 0 to 2 pi with 0 being up
            angle = (angle + pi/2) % (2 * pi)
            line_of_sights[angle].append(asteroid)
    return line_of_sights

def distance(locations: List[Location], station: Location) -> Dict[Location, float]:
    distances = {}
    for asteroid in locations:
        if asteroid != station:
            distances[asteroid] = (asteroid.X-station.X)**2 + (asteroid.Y-station.Y)**2
    return distances


def detection(locations: List[Location]) -> Dict[Location, int]:
    direct_detections = {}
    for asteroid in locations:
        neighbour = set()
        for target in locations:
            if target != asteroid:
                neighbour.add(atan2(target.Y-asteroid.Y, target.X-asteroid.X))
        direct_detections[asteroid] = len(neighbour)
    return direct_detections

def best_location(detections: Dict[Location, int]) -> Location:
    # return max(detections.keys(), key=lambda k: detections[k])
    return max(detections.items(), key=itemgetter(1))


def destroy_asteroid(locations: List[Location], station: Location) -> Iterator[Location]:

    line_of_sights = line_of_sight(locations, station)
    # sort by distance for each
    for los in line_of_sights.values():
        los.sort(key=lambda astr: abs(astr.X-station.X)+abs(astr.Y-station.Y), reverse=True)


    while line_of_sights:
        angles = line_of_sights.keys()
        angles = sorted(angles)

        for angle in angles:
            asteroids = line_of_sights[angle]
            yield asteroids.pop()
            if not asteroids:
                del line_of_sights[angle]



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

asteroids = parse_map(INPUT.split('\n'))
station, _ = best_location(detection(asteroids))
vaporized = list(destroy_asteroid(asteroids, station))
assert vaporized[0] == Location(11,12)
assert vaporized[1] == Location(12,1)
assert vaporized[2] == Location(12,2)
assert vaporized[-1] == Location(11,1)

"""
    The 1st asteroid to be vaporized is at 11,12.
    The 2nd asteroid to be vaporized is at 12,1.
    The 3rd asteroid to be vaporized is at 12,2.
    The 10th asteroid to be vaporized is at 12,8.
    The 20th asteroid to be vaporized is at 16,0.
    The 50th asteroid to be vaporized is at 16,9.
    The 100th asteroid to be vaporized is at 10,16.
    The 199th asteroid to be vaporized is at 9,6.
    The 200th asteroid to be vaporized is at 8,2.
    The 201st asteroid to be vaporized is at 10,9.
    The 299th and final asteroid to be vaporized is at 11,1.
"""

raw = """##.##..#.####...#.#.####
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

asteroids = parse_map(raw.split('\n'))
station, _ = best_location(detection(asteroids))
vaporized = list(destroy_asteroid(asteroids, station))
print(vaporized[199].X * 100 + vaporized[199].Y)