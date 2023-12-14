from dataclasses import dataclass
from typing import List, NamedTuple, Tuple, Dict
from collections import Counter
from tqdm import tqdm


RAW = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

RAW_3CYCLE = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""


class Pos(NamedTuple):
    x: int
    y: int


@dataclass
class Grid:
    cube_rocks: List[Pos]
    rounded_rocks: List[Pos]
    shape: Tuple[int, int]

    def __str__(self):
        lines = []
        for y in range(1, self.shape[0]):
            line = []
            for x in range(1, self.shape[1]):
                if Pos(x, y) in self.cube_rocks:
                    line.append("#")
                elif Pos(x, y) in self.rounded_rocks:
                    line.append("O")
                else:
                    line.append(".")
            lines.append("".join(line))
        return "\n".join(lines)

    def tilting_north(self) -> "Grid":
        rounded_rocks: List[Pos] = []

        for x in range(1, self.shape[1]):
            cubes = [item.y for item in self.cube_rocks if item.x == x]
            cubes.append(0)
            cubes.append(self.shape[0] + 1)
            cubes = sorted(cubes, reverse=True)

            roundeds = [item.y for item in self.rounded_rocks if item.x == x]
            roundeds = sorted(roundeds, reverse=True)

            for lo, hi in zip(cubes[1:], cubes[:-1]):
                within = [round for round in roundeds if lo <= round <= hi]
                if any(within):
                    for dy in range(len(within)):
                        rounded_rocks.append(Pos(x, lo + dy + 1))

        assert len(self.rounded_rocks) == len(rounded_rocks)
        return Grid(self.cube_rocks, rounded_rocks, self.shape)

    def tilting_south(self) -> "Grid":
        rounded_rocks: List[Pos] = []

        for x in range(1, self.shape[1]):
            cubes = [item.y for item in self.cube_rocks if item.x == x]
            cubes.append(0)
            cubes.append(self.shape[0])
            cubes = sorted(cubes)

            roundeds = [item.y for item in self.rounded_rocks if item.x == x]
            roundeds = sorted(roundeds)

            for hi, lo in zip(cubes[1:], cubes[:-1]):
                within = [round for round in roundeds if lo <= round <= hi]
                if any(within):
                    for dy in range(len(within)):
                        rounded_rocks.append(Pos(x, hi - dy - 1))

        assert len(self.rounded_rocks) == len(rounded_rocks)
        return Grid(self.cube_rocks, rounded_rocks, self.shape)

    def tilting_west(self) -> "Grid":
        rounded_rocks: List[Pos] = []

        for y in range(1, self.shape[0]):
            cubes = [item.x for item in self.cube_rocks if item.y == y]
            cubes.append(0)
            cubes.append(self.shape[1] + 1)
            cubes = sorted(cubes, reverse=True)

            roundeds = [item.x for item in self.rounded_rocks if item.y == y]
            roundeds = sorted(roundeds, reverse=True)

            for lo, hi in zip(cubes[1:], cubes[:-1]):
                within = [round for round in roundeds if lo <= round <= hi]
                if any(within):
                    for dx in range(len(within)):
                        rounded_rocks.append(Pos(lo + dx + 1, y))

        assert len(self.rounded_rocks) == len(rounded_rocks)
        return Grid(self.cube_rocks, rounded_rocks, self.shape)

    def tilting_east(self) -> "Grid":
        rounded_rocks: List[Pos] = []

        for y in range(1, self.shape[0]):
            cubes = [item.x for item in self.cube_rocks if item.y == y]
            cubes.append(0)
            cubes.append(self.shape[1])
            cubes = sorted(cubes)

            roundeds = [item.x for item in self.rounded_rocks if item.y == y]
            roundeds = sorted(roundeds)

            for hi, lo in zip(cubes[1:], cubes[:-1]):
                within = [round for round in roundeds if lo <= round <= hi]
                if any(within):
                    for dx in range(len(within)):
                        rounded_rocks.append(Pos(hi - dx - 1, y))

        assert len(self.rounded_rocks) == len(rounded_rocks)
        return Grid(self.cube_rocks, rounded_rocks, self.shape)

    def tilting_cycle(self) -> "Grid":
        return self.tilting_north().tilting_west().tilting_south().tilting_east()

    def load(self) -> int:
        load = 0
        for y, score in enumerate(range(self.shape[0], 0, -1)):
            load += score * len([item for item in self.rounded_rocks if item.y == y])
        return load

    @classmethod
    def from_raw(cls, raw: str) -> "Grid":
        cube_rocks: List[Pos] = []
        rounded_rocks: List[Pos] = []
        for y, line in enumerate(raw.splitlines(), start=1):
            for x, c in enumerate(line, start=1):
                if c == "#":
                    cube_rocks.append(Pos(x, y))
                elif c == "O":
                    rounded_rocks.append(Pos(x, y))

        return cls(cube_rocks, rounded_rocks, (y + 1, x + 1))


def part2(grid: Grid, cycle=1_000_000_000) -> int:
    # load on the north after 1_000_000_000
    # it as to be cyclic... let's generate 10 cycles

    loads = []
    lc = -1
    pbar = tqdm(leave=False)
    while True:
        grid = grid.tilting_cycle()
        loads.append(grid.load())
        c = Counter(loads)
        if lc == len(c) and c[min(loads)] > 4:
            break
        lc = len(c)
        pbar.update(1)

    # Find the burning phase...
    min_load = min(loads)
    indexes = [i for i, item in enumerate(loads) if item == min_load]
    burning_phase = indexes[0]
    # Check that after that we only have a cycle with the same phase
    period = indexes[1] - indexes[0]
    cycles = [(item - burning_phase) % period for item in indexes]
    assert all([item == 0 for item in cycles])
    # Compute the proper load
    return loads[burning_phase + (cycle - burning_phase) % period - 1]


GRID = Grid.from_raw(RAW)
assert GRID.tilting_north().load() == 136
assert str(GRID.tilting_cycle().tilting_cycle().tilting_cycle()) == RAW_3CYCLE
assert part2(GRID) == 64


with open("day14.txt", "r") as f:
    raw = f.read().strip()

grid = Grid.from_raw(raw)
print(grid.tilting_north().load())
print(part2(grid))
