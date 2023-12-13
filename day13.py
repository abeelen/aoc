from dataclasses import dataclass
from typing import List
from itertools import chain

RAW = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


@dataclass
class Pattern:
    data: List[List[int]]

    def __str__(self) -> str:
        return "\n".join(["".join(["#" if item == 1 else "." for item in row]) for row in self.data])

    @classmethod
    def parse_raw(cls, raw: str) -> "Pattern":
        data = [[1 if c == "#" else 0 for c in line] for line in raw.splitlines()]
        return cls(data)

    def find_vertical_reflection(self, data=None, part=1):
        if data is None:
            data = self.data
        length = len(data)
        for i in range(1, length):
            sub_length = min(i, length - i)
            upper = data[i - sub_length : i][::-1]
            lower = data[i : i + sub_length : 1]
            diff = sum([abs(u - l) for u, l in zip(chain.from_iterable(upper), chain.from_iterable(lower))])
            if diff + 1 == part:
                return i
        return 0

    def find_horizontal_reflection(self, part=1):
        data = [[row[i] for row in self.data] for i in range(len(self.data[0]))]
        return self.find_vertical_reflection(data=data, part=part)

    def score(self, part=1):
        return self.find_vertical_reflection(part=part) * 100 + self.find_horizontal_reflection(part=part)


PATTERNS = [Pattern.parse_raw(item) for item in RAW.split("\n\n")]
assert PATTERNS[0].find_vertical_reflection() == 0
assert PATTERNS[0].find_horizontal_reflection() == 5

assert PATTERNS[1].find_vertical_reflection() == 4
assert PATTERNS[1].find_horizontal_reflection() == 0
assert sum(item.score() for item in PATTERNS) == 405
assert sum(item.score(part=2) for item in PATTERNS) == 400


with open("day13.txt", "r") as f:
    raw = f.read().strip()

patterns = [Pattern.parse_raw(item) for item in raw.split("\n\n")]
print(sum(item.score() for item in patterns))
print(sum(item.score(part=2) for item in patterns))
