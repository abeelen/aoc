from typing import NamedTuple, List, Set

class XY(NamedTuple):
    x: int
    y: int

def locations(path: str) -> List[XY]:
    x = y = 0

    visited = [] # not including 0, 0

    for instruction in path.split(','):
        direction = instruction[0]
        steps = int(instruction[1:])

        for _ in range(steps):
            if direction == "R":
                x += 1
            elif direction == "L":
                x -= 1
            elif direction == "U":
                y += 1
            elif direction == "D":
                y -= 1
            else:
                raise ValueError("Bad direction : {}".format(direction))
       
            visited.append(XY(x, y))

    return visited

def crossing(path1: str, path2: str) -> Set[XY]:
    location1 = set(locations(path1))
    location2 = set(locations(path2))
    return location1.intersection(location2)

def manhattan_distance(xy: XY) -> int:
    return abs(xy.x) + abs(xy.y)

def distance(path1: str, path2: str) -> int:
    crosses = list(crossing(path1, path2))
    dist = [manhattan_distance(cross) for cross in crosses]
    return min(dist)

assert(distance("R8,U5,L5,D3", "U7,R6,D4,L4") == 6)
assert(distance("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83") == 159)

with open("input") as f:
    path1 = f.readline().strip()
    path2 = f.readline().strip()

print(distance(path1, path2))

def steps_to_cross(location1: List[XY], cross: XY) -> int:
    steps = 0
    while location1[steps] != cross:
        steps += 1 
    return steps + 1

def fewest_steps(path1: str, path2: str) -> int:
    location1 = locations(path1)
    location2 = locations(path2)
    crosses = list(set(location1).intersection(set(location2)))
    _steps = [steps_to_cross(location1, cross) + steps_to_cross(location2, cross) for cross in crosses]
    return min(_steps)

assert(fewest_steps("R8,U5,L5,D3", "U7,R6,D4,L4") == 30)
assert(fewest_steps("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83") == 610)
assert(fewest_steps("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") == 410)

print(fewest_steps(path1, path2))