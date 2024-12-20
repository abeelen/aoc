from collections import Counter, deque, namedtuple
from dataclasses import dataclass
from itertools import product
from typing import List, Set

Pos = namedtuple("Pos", ["x", "y"])
Race = namedtuple("Race", ["pos", "steps", "cheated"])


@dataclass
class Cpu:
    walls: Set[Pos]
    start: Pos
    end: Pos
    width: int = 0
    height: int = 0
    # They are too many walls to use the set approach... try the grid !
    grid: List[List[str]] = None

    def all_races(self) -> List[Race]:
        queue = deque([Race(self.start, 0, False)])
        visited = set()
        solutions = []

        while queue:
            current = queue.popleft()
            if (current.pos, current.cheated) in visited:
                continue

            if current.pos == self.end:
                if current.cheated:
                    solutions.append(current)
                else:
                    solutions.append(current)
                    return solutions

            visited.add((current.pos, current.cheated))

            for step in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = Pos(current.pos.x + step[0], current.pos.y + step[1])

                if new_pos in self.walls:
                    if current.cheated:
                        continue
                    else:
                        cheating_pos = Pos(current.pos.x + 2 * step[0], current.pos.y + 2 * step[1])
                        if (
                            cheating_pos in self.walls
                            or cheating_pos.x < 0
                            or cheating_pos.y < 0
                            or cheating_pos.x > self.width
                            or cheating_pos.y > self.height
                        ):
                            continue
                        else:
                            queue.append(Race(cheating_pos, current.steps + 2, new_pos))

                elif new_pos.x < 0 or new_pos.y < 0 or new_pos.x > self.width or new_pos.y > self.height:
                    continue
                else:
                    queue.append(Race(new_pos, current.steps + 1, current.cheated))

    # Brute force do not work... change strategy...

    def count_saves(self) -> int:
        solutions = self.all_races()
        max_steps = max([solution.steps for solution in solutions])
        return Counter([max_steps - solution.steps for solution in solutions if solution.steps != max_steps])

    def how_many_cheat(self, at_least: int) -> int:
        solutions = self.all_races()
        max_steps = max([solution.steps for solution in solutions])
        return len([solution for solution in solutions if solution.steps != max_steps and solution.steps >= at_least])

    def flood_fill(self, from_pos):
        # Retun length of all possible position seen from pos
        queue = deque([Race(from_pos, 0, None)])
        visited = {}

        while queue:
            current = queue.popleft()
            if current.pos in visited:
                continue

            visited[current.pos] = current.steps

            for step in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = Pos(current.pos.x + step[0], current.pos.y + step[1])

                if (
                    new_pos in self.walls
                    or new_pos.x < 0
                    or new_pos.y < 0
                    or new_pos.x > self.width
                    or new_pos.y > self.height
                ):
                    continue
                else:
                    queue.append(Race(new_pos, current.steps + 1, None))

        return visited

    # from https://git.sr.ht/~kwshi/advent-of-code/tree/main/item/python/2024/20.py

    def all_position_within(self, pos: Pos, distance: int) -> List[Pos]:
        output = []
        for dx, dy in product(range(-distance, distance + 1), repeat=2):
            if abs(dx) + abs(dy) <= distance:
                new_pos = Pos(pos.x + dx, pos.y + dy)
                if (
                    new_pos not in self.walls
                    and new_pos.x >= 0
                    and new_pos.y >= 0
                    and new_pos.x <= self.width
                    and new_pos.y <= self.height
                ):
                    output.append((new_pos, abs(dx) + abs(dy)))
        return output

    def race_with_cheat_distances(self, jump_up_to=2, at_least=100, return_count=True) -> int:
        distance_from_start = self.flood_fill(self.start)
        distance_from_end = self.flood_fill(self.end)
        # First get the best path without cheating
        distance_max = distance_from_start[self.end] - at_least

        good_cheats = []

        for i, j in product(range(self.width), range(self.height)):
            cheat_start = Pos(i, j)
            if cheat_start in self.walls:
                continue
            # Jump can be in  diagonal...
            for cheat_end, dist in self.all_position_within(cheat_start, jump_up_to):
                cheat_distance = distance_from_start[cheat_start] + dist + distance_from_end[cheat_end]
                if cheat_distance <= distance_max:
                    good_cheats.append([cheat_start, cheat_end, distance_from_start[self.end] - cheat_distance])
        if return_count:
            return len(good_cheats)
        else:
            return good_cheats

    @classmethod
    def from_raw(cls, input_raw: str) -> "Cpu":
        walls = set()
        start = None
        end = None
        for y, line in enumerate(input_raw.split("\n")):
            for x, char in enumerate(line):
                pos = Pos(x, y)
                if char == "#":
                    walls.add(pos)
                elif char == "S":
                    start = pos
                elif char == "E":
                    end = pos
        width = max([pos.x for pos in walls])
        height = max([pos.y for pos in walls])
        grid = [[item for item in line] for line in input_raw.split("\n")]
        return cls(walls, start, end, width, height, grid)


RAW_INPUT = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

CPU = Cpu.from_raw(RAW_INPUT)
"""
    There are 14 cheats that save 2 picoseconds.
    There are 14 cheats that save 4 picoseconds.
    There are 2 cheats that save 6 picoseconds.
    There are 4 cheats that save 8 picoseconds.
    There are 2 cheats that save 10 picoseconds.
    There are 3 cheats that save 12 picoseconds.
    There is one cheat that saves 20 picoseconds.
    There is one cheat that saves 36 picoseconds.
    There is one cheat that saves 38 picoseconds.
    There is one cheat that saves 40 picoseconds.
    There is one cheat that saves 64 picoseconds.
"""
SAVES = {2: 14, 4: 14, 6: 2, 8: 4, 10: 2, 12: 3, 20: 1, 36: 1, 38: 1, 40: 1, 64: 1}
assert CPU.count_saves() == SAVES
assert (
    Counter([item[2] for item in CPU.race_with_cheat_distances(jump_up_to=2, at_least=1, return_count=False)]) == SAVES
)
# MAX_STEPS = CPU.race(max_steps=False, can_cheat=False)[0].steps
# assert MAX_STEPS == 84
# assert len(CPU.race(max_steps=MAX_STEPS - 30, can_cheat=True)) == 4
# assert CPU.race_with_cheat(at_least=30) == 4
# assert CPU.grid_race_with_cheat(at_least=30) == 4
assert CPU.race_with_cheat_distances(jump_up_to=2, at_least=30) == 4
assert (
    CPU.race_with_cheat_distances(jump_up_to=20, at_least=50)
    == 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
)

with open("input/day20.txt", "r") as f:
    input_raw = f.read().strip()

cpu = Cpu.from_raw(input_raw)

# Does not work....  need to work backwards...
# print(cpu.how_many_cheat(at_least=100))
# max_steps = cpu.race(can_cheat=False)[0].steps
# print(cpu.race_with_cheat(at_least=100))
print(cpu.race_with_cheat_distances(jump_up_to=2, at_least=100))  # 1315 too low...
print(cpu.race_with_cheat_distances(jump_up_to=20, at_least=100))
