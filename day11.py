from typing import List, NamedTuple, Tuple
from dataclasses import dataclass

RAW = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


class Pos(NamedTuple):
    x: int
    y: int


@dataclass
class Universe:
    galaxies: List[Pos]
    shape: Tuple[int, int]

    def expand(self, expansion_factor: int = 1) -> None:
        # find row and column without galaxies
        rows = [i for i in range(self.shape[1]) if not any([True for pos in self.galaxies if pos.x == i])]
        cols = [j for j in range(self.shape[0]) if not any([True for pos in self.galaxies if pos.y == j])]
        for row in rows[::-1]:
            for idx, gal in enumerate(self.galaxies):
                if gal.x > row:
                    self.galaxies[idx] = Pos(gal.x + expansion_factor, gal.y)
        for col in cols[::-1]:
            for idx, gal in enumerate(self.galaxies):
                if gal.y > col:
                    self.galaxies[idx] = Pos(gal.x, gal.y + expansion_factor)

    def shortest_path(self, expansion_factor: int = 1) -> int:
        self.expand(expansion_factor=expansion_factor)
        distances = []
        for idx1, gal1 in enumerate(self.galaxies):
            for gal2 in self.galaxies[idx1 + 1 :]:
                distances.append(abs(gal2.x - gal1.x) + abs(gal2.y - gal1.y))
        return sum(distances)

    @classmethod
    def parse_raw(cls, raw: str) -> "Universe":
        galaxies = []
        for j, line in enumerate(raw.split("\n")):
            for i, c in enumerate(line):
                if c == "#":
                    galaxies.append(Pos(i, j))
        return cls(galaxies, shape=(j, i))


UNIVERSE = Universe.parse_raw(RAW)
assert UNIVERSE.shortest_path() == 374
UNIVERSE = Universe.parse_raw(RAW)
assert UNIVERSE.shortest_path(expansion_factor=9) == 1030
UNIVERSE = Universe.parse_raw(RAW)
assert UNIVERSE.shortest_path(expansion_factor=99) == 8410


with open("day11.txt", "r") as f:
    raw = f.read().strip()

universe = Universe.parse_raw(raw)
print(universe.shortest_path())

universe = Universe.parse_raw(raw)
print(universe.shortest_path(expansion_factor=1_000_000 - 1))
