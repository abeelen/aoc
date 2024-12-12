from collections import defaultdict, deque, namedtuple
from typing import Dict, List

RAW_INPUT = """AAAA
BBCD
BBCC
EEEC"""

Pos = namedtuple("Pos", ["x", "y"])


def define_regions(positions: List[Pos]) -> List[List[Pos]]:
    regions = []

    while positions:
        pos = positions.pop()
        region = [pos]
        queue = deque([pos])
        while queue:
            pos = queue.popleft()
            for delta in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                neighbour = Pos(pos.x + delta[0], pos.y + delta[1])
                if neighbour in positions:
                    region.append(neighbour)
                    positions.remove(neighbour)
                    queue.append(neighbour)
        regions.append(region)

    return regions


def parse_input(raw_input: str) -> Dict[str, List[Pos]]:
    grid = defaultdict(list)
    # 2 steps: first parse the full grid, then assign regions
    for y, line in enumerate(raw_input.split("\n")):
        for x, char in enumerate(line):
            grid[char].append(Pos(x, y))

    output = {}
    for key, positions in grid.items():
        regions = define_regions(positions)
        output[key] = regions[0]
        for i, region in enumerate(regions[1:]):
            output[key + str(i)] = region

    return output


def area(region: List[Pos]) -> int:
    return len(region)


def perimeter(region: List[Pos]) -> int:
    output = 0

    for pos in region:
        for delta in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            neighbour = Pos(pos.x + delta[0], pos.y + delta[1])
            if neighbour not in region:
                output += 1
    return output


def price(region: List[Pos]) -> int:
    return area(region) * perimeter(region)


def total_price(garden: Dict[str, List[Pos]]) -> int:
    return sum(price(region) for region in garden.values())


def sides(region: List[Pos]) -> int:
    # find the number of sides of the region
    # by counting the corners of the region
    # First classify the position of the regions
    # top : those who do not have a neighbour above
    # bottom : those who do not have a neighbour below
    # left : those who do not have a neighbour on the left
    # right : those who do not have a neighbour on the right

    top = [pos for pos in region if Pos(pos.x, pos.y + 1) not in region]
    bottom = [pos for pos in region if Pos(pos.x, pos.y - 1) not in region]
    left = [pos for pos in region if Pos(pos.x - 1, pos.y) not in region]
    right = [pos for pos in region if Pos(pos.x + 1, pos.y) not in region]

    # Not cound the corners by going though the top positions first
    corners = 0
    for pos in top:
        if pos in left:  # top left corner
            corners += 1
        if pos in right:  # top right corner
            corners += 1
        if pos not in left and Pos(pos.x - 1, pos.y + 1) in right:  # empty below but filled in the left diagonal
            corners += 1
        if pos not in right and Pos(pos.x + 1, pos.y + 1) in left:  # empty below but filled in the right diagonal
            corners += 1
    # and the bottom positions
    for pos in bottom:
        if pos in left:  # bottom left corner
            corners += 1
        if pos in right:  # bottom right corner
            corners += 1
        if pos not in left and Pos(pos.x - 1, pos.y - 1) in right:  # empty above but filled in the left diagonal
            corners += 1
        if pos not in right and Pos(pos.x + 1, pos.y - 1) in left:
            corners += 1

    return corners


def new_price(region: List[Pos]) -> int:
    return area(region) * sides(region)


def new_total_price(garden: Dict[str, List[Pos]]) -> int:
    return sum(new_price(region) for region in garden.values())


GARDEN = parse_input(RAW_INPUT)
assert len(GARDEN) == 5
assert perimeter(GARDEN["A"]) == 10
assert perimeter(GARDEN["C"]) == 10
assert perimeter(GARDEN["B"]) == 8
assert perimeter(GARDEN["E"]) == 8
assert perimeter(GARDEN["D"]) == 4
assert price(GARDEN["A"]) == 40
assert price(GARDEN["B"]) == 32
assert price(GARDEN["C"]) == 40
assert price(GARDEN["D"]) == 4
assert price(GARDEN["E"]) == 24
assert total_price(GARDEN) == 140
assert sides(GARDEN["A"]) == 4
assert sides(GARDEN["B"]) == 4
assert sides(GARDEN["C"]) == 8
assert sides(GARDEN["D"]) == 4
assert sides(GARDEN["E"]) == 4
assert new_total_price(GARDEN) == 80

RAW_INPUT = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

GARDEN = parse_input(RAW_INPUT)
assert perimeter(GARDEN["O"]) == 36
assert perimeter(GARDEN["X"]) == 4
assert area(GARDEN["X"]) == 1
assert price(GARDEN["O"]) == 756
assert price(GARDEN["X"]) == 4
assert total_price(GARDEN) == 772
assert new_total_price(GARDEN) == 436

RAW_INPUT = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

GARDEN = parse_input(RAW_INPUT)
assert total_price(GARDEN) == 1930

RAW_INPUT = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
GARDEN = parse_input(RAW_INPUT)
assert new_total_price(GARDEN) == 236

RAW_INPUT = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
GARDEN = parse_input(RAW_INPUT)
assert new_total_price(GARDEN) == 368


with open("day12.txt", "r") as file:
    raw_input = file.read().strip()

garden = parse_input(raw_input)
print(total_price(garden))
print(new_total_price(garden))
