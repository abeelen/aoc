from collections import defaultdict, namedtuple
from itertools import product
from typing import Dict, List

RAW_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

Pos = namedtuple("Pos", ["x", "y"])


def parse_input(data: str, match: str) -> Dict[str, List[Pos]]:
    lines = data.split("\n")

    letters = defaultdict(list)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char in match:
                letters[char].append(Pos(i, j))
    return letters


def find_XMAS(letters: Dict[str, List[Pos]]) -> int:
    n = 0

    for pos in letters["X"]:
        for direction in product([-1, 0, 1], [-1, 0, 1]):
            if all(
                [
                    Pos(pos.x + direction[0] * i, pos.y + direction[1] * i) in letters[letter]
                    for i, letter in enumerate("MAS", 1)
                ]
            ):
                n += 1
    return n


def find_X_MAS(letters: Dict[str, List[Pos]]) -> int:
    n = 0
    for pos in letters["A"]:
        found = 0
        for direction in product([-1, 1], [-1, 1]):
            if all(
                [
                    Pos(pos.x + direction[0] * i, pos.y + direction[1] * i) in letters[letter]
                    for i, letter in zip([-1, 1], "MS")
                ]
            ):
                found += 1
        if found == 2:
            n += 1
    return n


assert find_XMAS(parse_input(RAW_INPUT, "XMAS")) == 18
assert find_X_MAS(parse_input(RAW_INPUT, "XMAS")) == 9

with open("day04.txt", "r") as f:
    data = f.read().strip()

print(find_XMAS(parse_input(data, "XMAS")))
print(find_X_MAS(parse_input(data, "XMAS")))
