from collections import namedtuple
from dataclasses import dataclass
from typing import List, Dict, Tuple, NamedTuple
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

# Pos = namedtuple("Pos", ("x", "y"))

class Pos(NamedTuple):
    x: int
    y: int

@dataclass
class Number:
    start: Pos
    end: Pos
    value: int

    
def adjacent_to_number(loc: Pos, number: Number) -> bool:
    nx_lo, nx_hi = number.start.x, number.end.x
    ny = number.start.y
    
    x, y = loc
    
    return nx_lo - 1 <= x <= nx_hi + 1 and ny - 1 <= y <= ny + 1

@dataclass
class Schematic:
    numbers: List[Number]
    symbols: Dict[Pos, str]

    @classmethod
    def parse_raw(cls, raw: str) -> "Schematic":
        symbols = {}
        numbers = []
        for i, line in enumerate(raw.split("\n")):
            for number in re.finditer("\d*", line):
                if number.group() == "":
                    continue
                numbers.append(Number(Pos(number.start(), i), Pos(number.end() - 1, i), int(number.group())))
            for j, c in enumerate(line):
                if c.isdigit() or c == ".":
                    continue
                symbols[Pos(j, i)] =  c

        return cls(numbers, symbols)

    def part_numbers(self) -> List[int]:
        return [number.value for number in self.numbers if self.is_adjacent_to_symbols(number)]
    
    def is_adjacent_to_symbols(self, number: Number) -> bool:
        return any([adjacent_to_number(loc, number) for loc in self.symbols])
    
    def gear_ratios(self) -> List[int]:
        locs = [pos for pos, symbol in self.symbols.items() if symbol == '*']
        output = []

        for loc in locs:
            adjacent_numbers = [n for n in self.numbers if adjacent_to_number(loc, n)]             
            if len(adjacent_numbers) == 2:
                output.append(adjacent_numbers[0].value * adjacent_numbers[1].value)
        return output
    
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


SCHEME = Schematic.parse_raw(RAW)
assert sum(SCHEME.part_numbers()) == 4361
assert sum(SCHEME.gear_ratios()) == 467835



with open("day03.txt", "r") as f:
    raw = f.read()

schematic = Schematic.parse_raw(raw)
print(sum(schematic.part_numbers()))
print(sum(schematic.gear_ratios()))


SYMBOLS, NUMBERS = parse_schematic(RAW)
assert sum([int(number[0]) for number in NUMBERS if is_part_number(number, SYMBOLS)]) == 4361
assert sum([gear_ratio(symbol, NUMBERS) for symbol in SYMBOLS]) == 467835

symbols, numbers = parse_schematic(raw)
print(sum([int(number[0]) for number in numbers if is_part_number(number, symbols)]))
print(sum([gear_ratio(symbol, numbers) for symbol in symbols]))
