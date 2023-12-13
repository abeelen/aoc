from collections import deque

def parse_raw(raw: str) -> set:
    return set([tuple(int(item) for item in line.split(',')) for line in raw.splitlines()])


def count_exposed_sides(raw:str) -> int:
    cubes = parse_raw(raw)

    faces = 0
    for cube in cubes:
        x, y, z = cube
        for dx, dy, dz in [(+1, 0, 0), (-1, 0, 0), 
                           (0, +1, 0), (0, -1, 0),
                           (0, 0, +1), (0, 0, -1)]:
            if (x + dx, y + dy, z + dz) not in cubes:
                faces += 1
    return faces


def can_escape(x, y, z, cubes):
    # BFS type
    x_min = min([item[0] for item in cubes])
    x_max = max([item[0] for item in cubes])
    y_min = min([item[1] for item in cubes])
    y_max = max([item[1] for item in cubes])
    z_min = min([item[2] for item in cubes])
    z_max = max([item[2] for item in cubes])

    queue = deque()
    queue.append((x, y, z))
    visited = set()
    while queue:
        x, y, z = queue.popleft()
        if (x, y, z) in visited:
            continue
        visited.add((x, y, z))
        if (x, y, z) in cubes:
            # BAM a rock
            continue
        if (x < x_min or x > x_max or
            y < y_min or y > y_max or
            z < z_min or z > z_max ):
            # we are out !
            return True
        for dx, dy, dz in [(+1, 0, 0), (-1, 0, 0), 
                           (0, +1, 0), (0, -1, 0),
                           (0, 0, +1), (0, 0, -1)]:
            queue.append((x + dx, y + dy, z + dz))

    return False


def count_exterior_surface_area(raw:str) -> int:

    ## Brute force : 
    cubes = parse_raw(raw)
    faces = 0
    for cube in cubes:
        x, y, z = cube
        for dx, dy, dz in [(+1, 0, 0), (-1, 0, 0), 
                           (0, +1, 0), (0, -1, 0),
                           (0, 0, +1), (0, 0, -1)]:
            if can_escape(x + dx, y + dy, z + dz, cubes):
                faces += 1

    # WRONG !! Some could be multiple pockes
    # # exposed sides : 
    # exposed = count_exposed_sides(raw)
    # # Find the empty cells which can not get out
    # cubes = parse_raw(raw)
    
    # x_min = min([item[0] for item in cubes])
    # x_max = max([item[0] for item in cubes])
    # y_min = min([item[1] for item in cubes])
    # y_max = max([item[1] for item in cubes])
    # z_min = min([item[2] for item in cubes])
    # z_max = max([item[2] for item in cubes])

    # trapped = 0
    # for x in range(x_min, x_max):
    #     for y in range(y_min, y_max):
    #         for z in range(z_min, z_max):
    #             if (x, y, z) not in cubes and (not can_escape(x,y,z, cubes)):
    #                     trapped += 1
    
    # faces = exposed - trapped * 6

    return faces


RAW="""1,1,1
2,1,1"""

assert count_exposed_sides(RAW) == 10

RAW="""2,2,2
1,2,2
3,2,2
2,1,2   
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

assert count_exposed_sides(RAW) == 64
assert count_exterior_surface_area(RAW) == 58

with open('day18.txt') as f:
    raw = f.read()

print(count_exposed_sides(raw))
print(count_exterior_surface_area(raw))