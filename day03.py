from collections import namedtuple
from typing import List, Dict, Tuple
import re

RAW = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

Pos = namedtuple("Pos", ("x", "y"))


def parse_schematic(raw: str):
    symbols = []
    numbers = []
    for i, line in enumerate(raw.split("\n")):
        for number in re.finditer("\d*", line):
            if number.group() == "":
                continue
            numbers.append((number.group(), Pos(number.start(), i)))
        for j, c in enumerate(line):
            if c.isdigit() or c == ".":
                continue
            symbols.append((c, Pos(j, i)))

    return symbols, numbers


from math import sqrt


def distance(p1: Pos, p2: Pos) -> int:
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def distance_to_number(pos, number):
    label, start_pos = number
    return min([distance(Pos(start_pos.x + offset, start_pos.y), pos) for offset in range(len(label))])


def is_part_number(number, symbols) -> bool:
    return any([distance_to_number(symbol[1], number) < 2 for symbol in symbols])


def is_gear(symbol, numbers) -> bool:
    label, pos = symbol
    if label != "*":
        return False
    return sum([distance_to_number(symbol[1], number) < 2 for number in NUMBERS]) == 2


def gear_ratio(symbol, numbers) -> int:
    label, pos = symbol
    if label != "*":
        return 0
    number_ids = [int(number[0]) for number in numbers if distance_to_number(symbol[1], number) < 2]
    if len(number_ids) != 2:
        return 0
    return number_ids[0] * number_ids[1]


SYMBOLS, NUMBERS = parse_schematic(RAW)
assert sum([int(number[0]) for number in NUMBERS if is_part_number(number, SYMBOLS)]) == 4361
assert sum([gear_ratio(symbol, NUMBERS) for symbol in SYMBOLS]) == 467835


with open("day03.txt", "r") as f:
    raw = f.read()

symbols, numbers = parse_schematic(raw)
print(sum([int(number[0]) for number in numbers if is_part_number(number, symbols)]))
print(sum([gear_ratio(symbol, numbers) for symbol in symbols]))
