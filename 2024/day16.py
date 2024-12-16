import heapq
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from typing import NamedTuple, Set, Tuple


class Pos(NamedTuple):
    x: int
    y: int


TURNS = {
    "E": ["N", "S"],
    "W": ["S", "N"],
    "N": ["W", "E"],
    "S": ["E", "W"],
}
DIRECTIONS = {"E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1)}
WALL = "#"
START = "S"
END = "E"


@dataclass
class Maze:
    start_pos: Pos
    end_pos: Pos
    wall: Set[Pos]
    shape: Tuple[int, int]

    # Dijkstra dequeue works for examples but not for the real world... very long...
    # -> heapq, but still super long !!!!
    def lowest_score(self, direction: str = "E") -> int:
        queue = [(0, self.start_pos, direction)]
        visited = set()
        while queue:
            score, pos, direction = heapq.heappop(queue)
            if pos == self.end_pos:
                return score

            visited.add((pos, direction))

            # Move forward
            speed = DIRECTIONS[direction]
            new_pos = Pos(pos.x + speed[0], pos.y + speed[1])
            new_score = score + 1
            if (new_pos, direction) not in visited and new_pos not in self.wall:
                heapq.heappush(queue, (new_score, new_pos, direction))

            # Turns
            for direction in TURNS[direction]:
                speed = DIRECTIONS[direction]
                new_pos = Pos(pos.x + speed[0], pos.y + speed[1])
                new_score = score + 1001
                if (new_pos, direction) not in visited and new_pos not in self.wall:
                    heapq.heappush(queue, (new_score, new_pos, direction))

    def spot_to_sit_on(self, direction: str = "E", lowest_score=float("inf")) -> int:
        queue = [(0, self.start_pos, direction, [])]
        visited = set()
        good_path = defaultdict(list)
        while queue:
            score, pos, direction, path = heapq.heappop(queue)
            if score > lowest_score:
                continue

            if pos == self.end_pos:
                lowest_score = min(lowest_score, score)
                good_path[score].append(path)
                continue

            visited.add((pos, direction))
            path = [*path, pos]

            # Move forward
            speed = DIRECTIONS[direction]
            new_pos = Pos(pos.x + speed[0], pos.y + speed[1])
            new_score = score + 1
            if (new_pos, direction) not in visited and new_pos not in self.wall:
                heapq.heappush(queue, (new_score, new_pos, direction, path))

            # Turns
            for direction in TURNS[direction]:
                speed = DIRECTIONS[direction]
                new_pos = Pos(pos.x + speed[0], pos.y + speed[1])
                new_score = score + 1001
                if (new_pos, direction) not in visited and new_pos not in self.wall:
                    heapq.heappush(queue, (new_score, new_pos, direction, path))

        return len(set(chain.from_iterable(good_path[lowest_score]))) + 1

    @classmethod
    def parse_raw(cls, raw_input: str) -> "Maze":
        raw_input = raw_input.strip()
        start_pos = None
        end_pos = None
        wall = []
        for y, line in enumerate(raw_input.split("\n")):
            for x, char in enumerate(line):
                if char == "S":
                    start_pos = Pos(x, y)
                elif char == "E":
                    end_pos = Pos(x, y)
                elif char == WALL:
                    wall.append(Pos(x, y))
        return cls(start_pos, end_pos, set(wall), (len(line), len(raw_input.split("\n"))))


RAW_INPUT = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

MAZE = Maze.parse_raw(RAW_INPUT)
assert MAZE.lowest_score() == 7036
assert MAZE.spot_to_sit_on(lowest_score=7036) == 45

RAW_INPUT = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

MAZE = Maze.parse_raw(RAW_INPUT)
assert MAZE.lowest_score() == 11048
assert MAZE.spot_to_sit_on(lowest_score=11048) == 64


with open("day16.txt", "r") as file:
    raw_input = file.read().strip()

maze = Maze.parse_raw(raw_input)
print(maze.lowest_score())  # 111488
print(maze.spot_to_sit_on(lowest_score=111480))

# There are many walls, so maybe not so clever to store walls and set againts a list, sets are faster
# However using a 2d array might be faster
