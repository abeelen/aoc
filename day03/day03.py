from __future__ import annotations
from typing import Set, Tuple, NamedTuple
import math

RAW = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

Point = Tuple[int, int]


class TreeMap(NamedTuple):
    trees: Set[Point]
    width: int
    height: int

    @staticmethod
    def parse(raw: str) -> TreeMap:
        lines = raw.split("\n")
        trees = [
            (x, y)
            for y, line in enumerate(lines)
            for x, c in enumerate(line.strip())
            if c == "#"
        ]
        height = len(lines)
        width = len(lines[0].strip())

        return TreeMap(trees, width, height)


TREEMAP = TreeMap.parse(RAW)


def count_trees(treemap: TreeMap, right: int = 3, down: int = 1) -> int:
    num_trees = 0
    x = 0
    for y in range(0, treemap.height, down):
        if (x, y) in treemap.trees:
            num_trees += 1
        x = (x + right) % treemap.width
    return num_trees


def count_tree(map_grid: List[str], dx: int, dy: int) -> int:
    n_lines = len(map_grid)
    n_rows = len(map_grid[0])
    x_steps = [(step * dx) % n_rows for step in range(n_lines // dy)]
    y_steps = [step * dy for step in range(n_lines // dy)]

    trace = [map_grid[y][x] for x, y in zip(x_steps, y_steps)]
    return "".join(trace).count("#")


RAW = RAW.split("\n")
assert count_tree(RAW, 3, 1) == 7
assert count_trees(TREEMAP, 3, 1) == 7

with open("day03.txt") as f:
    raw = f.read()

treemap = TreeMap.parse(raw)
print(count_trees(treemap, 3, 1))
# %timeit count_trees(treemap, 3, 1)
grid = [line.strip() for line in raw.split("\n") if line]
print(count_tree(grid, 3, 1))
# %timeit count_tree(grid, 3, 1)

SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
assert math.prod([count_tree(RAW, *slope) for slope in SLOPES]) == 336

print(math.prod([count_tree(grid, *slope) for slope in SLOPES]))
print(math.prod([count_trees(treemap, *slope) for slope in SLOPES]))