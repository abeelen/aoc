from dataclasses import dataclass, field
from typing import List
from itertools import chain

@dataclass
class Assignements():
    section: List[int] = field(default_factory=list)

    @classmethod
    def from_string(cls, input):
        start, end = input.split('-')
        return cls(section = list(range(int(start), int(end)+1)))

@dataclass
class ElvesPair():
    elves: List[Assignements]


    def is_fully_contains(self):
        section_lengths = [len(elve.section) for elve in self.elves]
        section_union = set(chain.from_iterable([elve.section for elve in self.elves]))
        if len(section_union) == max(section_lengths):
            return True
        else:
            return False

    def do_overlap(self):
        section_lengths = [len(elve.section) for elve in self.elves]
        section_union = set(chain.from_iterable([elve.section for elve in self.elves]))
        if len(section_union) < sum(section_lengths):
            return True
        else:
            return False
       

    @classmethod
    def from_line(cls, line):
        return cls(elves=[Assignements.from_string(item) for item in line.split(',')])


def parse_assignements(lines):
    return sum([ElvesPair.from_line(line.strip()).is_fully_contains() for line in lines.strip().split('\n')])


def parse_assignements2(lines):
    return sum([ElvesPair.from_line(line.strip()).do_overlap() for line in lines.strip().split('\n')])

RAW="""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

assert parse_assignements(RAW) == 2
assert parse_assignements2(RAW) == 4

with open('day04.txt', 'r') as f:
    lines = f.read()

print(parse_assignements(lines))
print(parse_assignements2(lines))