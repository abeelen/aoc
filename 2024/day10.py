from collections import (
    defaultdict,
    deque,
    namedtuple,
)
from typing import (
    List,
)

RAW_INPUT = """0123
1234
8765
9876"""

RAW_INPUT_2 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

Pos = namedtuple(
    "Pos",
    [
        "x",
        "y",
    ],
)


def parse_input(
    raw_input: str,
) -> List[List[int]]:
    lines = raw_input.strip().split("\n")
    grid = [[int(c) for c in line] for line in lines]
    return grid


def find_starts(
    grid: List[List[int]],
) -> List[Pos]:
    starts = []
    for (
        y,
        line,
    ) in enumerate(grid):
        for (
            x,
            h,
        ) in enumerate(line):
            if h == 0:
                starts.append(
                    Pos(
                        x,
                        y,
                    )
                )
    return starts


def score_trailheads(
    grid: List[List[int]],
    rating=False,
) -> int:
    starts = find_starts(grid)
    max_x = len(grid[0])
    max_y = len(grid)

    trailheads = defaultdict(list)
    queue = deque([[item] for item in starts])
    while queue:
        trail = queue.popleft()

        last_pos = trail[-1]
        height = grid[last_pos.y][last_pos.x]

        for (
            dx,
            dy,
        ) in (
            (
                -1,
                0,
            ),
            (
                1,
                0,
            ),
            (
                0,
                -1,
            ),
            (
                0,
                1,
            ),
        ):
            new_pos = Pos(
                last_pos.x + dx,
                last_pos.y + dy,
            )
            if 0 <= new_pos.x < max_x and 0 <= new_pos.y < max_y:
                new_height = grid[new_pos.y][new_pos.x]
                if new_height == height + 1:
                    new_trail = trail + [new_pos]
                    if new_height == 9 and (rating or new_pos not in trailheads[trail[0]]):
                        trailheads[trail[0]].append(new_pos)
                    else:
                        queue.append(new_trail)

    return sum([len(value) for value in trailheads.values()])


assert score_trailheads(parse_input(RAW_INPUT)) == 1
assert score_trailheads(parse_input(RAW_INPUT_2)) == 36
assert (
    score_trailheads(
        parse_input(RAW_INPUT_2),
        rating=True,
    )
    == 81
)

with open(
    "day10.txt",
    "r",
) as file:
    raw_input = file.read()

print(score_trailheads(parse_input(raw_input)))
print(
    score_trailheads(
        parse_input(raw_input),
        rating=True,
    )
)
