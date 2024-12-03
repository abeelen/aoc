from collections import deque
import heapq

from typing import List, NamedTuple

RAW = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

# That will be a graph theory thingy... BFS from last year ?? Dijkstra ? deque - heapq


def parse_raw(raw: str) -> List[List[int]]:
    return [[int(c) for c in line] for line in raw.split("\n")]


class Pos(NamedTuple):
    x: int
    y: int


Dir = Pos
DIRS = [Dir(0, 1), Dir(1, 0), Dir(0, -1), Dir(-1, 0)]


class Path(NamedTuple):
    cost: int
    pos: Pos
    dir_index: int
    dir_count: int
    history: List[Pos]

def plot_state(grid: List[List[int]], paths: List[Path], i=0):
    import matplotlib.pyplot as plt
    import numpy as np
    
    plt.clf()
    plt.imshow(np.array(grid), )
    for path in paths:
        plt.plot(*np.array(path.history).T, linewidth=2, c='orange', alpha=0.5)
    plt.savefig(f'day17_{i:05d}.png', dpi=300)

# ffmpeg -i day17_%05d.png output.mp4



def dijkstra(grid: List[List[int]], max_dir=3, min_dir=1, history=False):
    start = Pos(0, 0)
    end = Pos(len(grid[0]) - 1, len(grid) - 1)

    # we start from the (0,0) position with all directions
    heaplist = [Path(0, start, dir, 1, [start]) for dir in range(4)]
    seen = set()
    
    i = 0
    while heaplist:
        if history:
            plot_state(grid, heaplist, i)
            i += 1
        path = heapq.heappop(heaplist)
        if path.pos == end and path.dir_count > min_dir:
            # Arrived !!!
            if history:
                return path.cost, path.history
            else:
                return path.cost

        if (path.pos, path.dir_index, path.dir_count) in seen:
            # We were there before
            continue

        seen.add((path.pos, path.dir_index, path.dir_count))

        new_pos = Pos(path.pos.x + DIRS[path.dir_index].x, path.pos.y + DIRS[path.dir_index].y)

        # Can not go out of the grid
        if new_pos.x < 0 or new_pos.y < 0 or end.x < new_pos.x or end.y < new_pos.y:
            continue

        new_cost = path.cost + grid[new_pos.y][new_pos.x]

        # Add all possible directions
        for dir_index in range(4):
            if dir_index == ((path.dir_index + 2) % 4):
                # Can not go back
                continue

            if (dir_index != path.dir_index) and (path.dir_count < min_dir):
                # Cat not change direction if we do not have at least min_dir
                continue

            new_count = path.dir_count + 1 if dir_index == path.dir_index else 1

            if new_count > max_dir:
                # Can not go in that direction anymore
                continue

            heapq.heappush(heaplist, Path(new_cost, new_pos, dir_index, new_count, path.history+ [new_pos,]))

    return None


WORLD = parse_raw(RAW)
assert dijkstra(WORLD, max_dir=3, min_dir=1) == 102
assert dijkstra(WORLD, max_dir=10, min_dir=4) == 94

cost, history = dijkstra(WORLD, history=True)
 
RAW = """111111111111
999999999991
999999999991
999999999991
999999999991"""
WORLD = parse_raw(RAW)
assert dijkstra(WORLD, max_dir=10, min_dir=4) == 71


with open("day17.txt", "r") as f:
    raw = f.read().strip()

world = parse_raw(raw)
# cost, history = dijkstra(world, max_dir=3, min_dir=1, history=True)
#print(dijkstra(world, max_dir=3, min_dir=1))
# print(dijkstra(world, max_dir=10, min_dir=4))
