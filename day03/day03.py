from typing import List
import math

MAP="""..##.......
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

MAP = MAP.split('\n')

def count_tree(map_grid: List[str], dx: int, dy:int) -> int:
    n_lines = len(map_grid)
    n_rows = len(map_grid[0])
    x_steps = [(step * dx) % n_rows for step in range(n_lines // dy)]
    y_steps = [step * dy for step in range(n_lines // dy)]

    trace = [map_grid[y][x] for x,y in zip(x_steps, y_steps)]
    return ''.join(trace).count('#')

assert count_tree(MAP, 3, 1) == 7

with open('day03.txt') as f:
    grid = [line.strip() for line in f]
    print(count_tree(grid, 3, 1))


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1,2)]
assert math.prod([count_tree(MAP, *slope) for slope in slopes]) == 336

print(math.prod([count_tree(grid, *slope) for slope in slopes])
