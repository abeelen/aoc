from collections import defaultdict, namedtuple
from itertools import combinations
from math import ceil
from typing import Dict, List, Tuple

RAW_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

RAW_INPUT_T = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""

Pos = namedtuple("Pos", ["x", "y"])
Size = Pos


def parse_input(raw_input: str) -> Tuple[Dict[str, List[Pos]], Size]:
    output = defaultdict(list)
    lines = raw_input.split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                output[char].append(Pos(x, y))

    return output, Size(len(lines[0]), len(lines))


def compute_antinodes(pos: List[Pos], size: Size, harmonics=False) -> List[Pos]:
    antinodes = []
    for pos1, pos2 in combinations(pos, 2):
        if pos1 == pos2:
            continue
        dx = pos2.x - pos1.x
        dy = pos2.y - pos1.y

        if harmonics:
            harmonics = ceil(min(size.x / abs(dx), size.y / abs(dy)))
            nodes = [Pos(pos1.x + dx * factor, pos1.y + dy * factor) for factor in range(-harmonics - 1, harmonics + 1)]
        else:
            nodes = [
                Pos(pos1.x - dx, pos1.y - dy),
                Pos(pos1.x + 2 * dx, pos1.y + 2 * dy),
            ]
        # nodes = [
        #     Pos(pos1.x - dx * factor, pos1.y - dy * factor)
        #     for factor in range(1, harmonics + 1)
        # ] + [
        #     Pos(pos1.x + dx * factor, pos1.y + dy * factor)
        #     for factor in range(2, harmonics + 2)
        # ]
        #
        for node in nodes:
            if 0 <= node.x < size.x and 0 <= node.y < size.y:
                antinodes.append(node)
    return antinodes


def compute_unique_antinodes(data: Dict[str, List[Pos]], size: Size, harmonics=False) -> int:
    output = set()
    for pos in data.values():
        antinodes = compute_antinodes(pos, size, harmonics=harmonics)
        output.update(antinodes)
    return len(output)


assert compute_unique_antinodes(*parse_input(RAW_INPUT)) == 14
assert compute_unique_antinodes(*parse_input(RAW_INPUT_T), harmonics=True) == 9
assert compute_unique_antinodes(*parse_input(RAW_INPUT), harmonics=True) == 34

with open("day08.txt") as f:
    raw = f.read().strip()

print(compute_unique_antinodes(*parse_input(raw)))
print(compute_unique_antinodes(*parse_input(raw), harmonics=True))
