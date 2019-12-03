from typing import NamedTuple, List, Set

class XY(NamedTuple):
    x: int
    y: int

def locations(path: str) -> List[XY]:
    xys = [XY(0, 0)]
    for instr in path.split(','):
        direction, steps = instr[0], int(instr[1:])
        pos = xys[-1]
        if direction == "R":
            for i in range(1, steps+1):
                xys.append(XY(pos.x+i, pos.y))
        elif direction == "L":
            for i in range(1, steps+1):
                xys.append(XY(pos.x-i, pos.y))
        elif direction == "U":
            for i in range(1, steps+1):
                xys.append(XY(pos.x, pos.y+i))
        elif direction == "D":
            for i in range(1, steps+1):
                xys.append(XY(pos.x, pos.y-i))
    return xys

def crossing(path1: str, path2: str) -> Set[XY]:
    pos1 = locations(path1)
    pos2 = locations(path2)
    return set(pos1).intersection(set(pos2))

def distance(path1: str, path2: str) -> int:
    crosses = list(crossing(path1, path2))
    dist = [abs(cross.x)+abs(cross.y) for cross in crosses if cross != XY(0,0)]
    return min(dist)

assert(distance("R8,U5,L5,D3", "U7,R6,D4,L4") == 6)
assert(distance("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83") == 159)

with open("input") as f:
    path1 = f.readline().strip()
    path2 = f.readline().strip()

print(distance(path1, path2))

def steps(pos1: List[XY], cross: XY) -> int:
    steps = 0
    while pos1[steps] != cross:
        steps += 1 
    return steps

def fewest_steps(path1: str, path2: str) -> int:
    pos1 = locations(path1)
    pos2 = locations(path2)
    crosses = list(set(pos1).intersection(set(pos2)))
    _steps = [steps(pos1, cross) + steps(pos2, cross) for cross in crosses if cross != XY(0,0)]
    return min(_steps)

assert(fewest_steps("R8,U5,L5,D3", "U7,R6,D4,L4") == 30)
assert(fewest_steps("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83") == 610)
assert(fewest_steps("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") == 410)

print(fewest_steps(path1, path2))