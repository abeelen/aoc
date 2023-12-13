from typing import NamedTuple, List, Dict, Tuple
from dataclasses import dataclass


class Pos(NamedTuple):
    x: int
    y: int


@dataclass
class Tile:
    pos: Pos
    pipe: str

    def next(self, prev: Pos) -> Pos:
        # What if we can not move there
        dx = self.pos.x - prev.x
        dy = self.pos.y - prev.y
        if self.pipe == "|" and dx == 0:
            return Pos(self.pos.x, self.pos.y + dy)
        elif self.pipe == "-" and dy == 0:
            return Pos(self.pos.x + dx, self.pos.y)
        elif self.pipe == "L" and dx <= 0 and dy >= 0:
            return Pos(self.pos.x + dy, self.pos.y + dx)
        elif self.pipe == "J" and dx >= 0 and dy >= 0:
            return Pos(self.pos.x - dy, self.pos.y - dx)
        elif self.pipe == "7" and dx >= 0 and dy <= 0:
            return Pos(self.pos.x + dy, self.pos.y + dx)
        elif self.pipe == "F" and dx <= 0 and dy <= 0:
            return Pos(self.pos.x - dy, self.pos.y - dx)
        else:
            return None


"""
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""


assert Tile(Pos(1, 1), "-").next(Pos(0, 1)) == Pos(2, 1)
assert Tile(Pos(1, 1), "-").next(Pos(2, 1)) == Pos(0, 1)

assert Tile(Pos(1, 1), "|").next(Pos(1, 0)) == Pos(1, 2)
assert Tile(Pos(1, 1), "|").next(Pos(1, 2)) == Pos(1, 0)

assert Tile(Pos(2, 1), "L").next(Pos(2, 0)) == Pos(3, 1)
assert Tile(Pos(2, 1), "L").next(Pos(3, 1)) == Pos(2, 0)

assert Tile(Pos(2, 1), "J").next(Pos(2, 0)) == Pos(1, 1)
assert Tile(Pos(2, 1), "J").next(Pos(1, 1)) == Pos(2, 0)

assert Tile(Pos(2, 1), "7").next(Pos(1, 1)) == Pos(2, 2)
assert Tile(Pos(2, 1), "7").next(Pos(2, 2)) == Pos(1, 1)

assert Tile(Pos(2, 1), "F").next(Pos(3, 1)) == Pos(2, 2)
assert Tile(Pos(2, 1), "F").next(Pos(2, 2)) == Pos(3, 1)


@dataclass
class Tiles:
    tiles: Dict[Pos, Tile]
    start: Pos
    shape: Tuple[int, int]

    def find_start_direction(self):
        # We need to find the direction of the starting position
        start_dir = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            test_pos = Pos(self.start.x + dx, self.start.y + dy)
            if test_pos in self.tiles and self.tiles[test_pos].next(self.start) is not None:
                start_dir.append((dx, dy))
        return start_dir

    def explore_path(self) -> List[Pos]:
        start_directions = self.find_start_direction()
        assert len(start_directions) == 2
        start_directions = start_directions[0]
        path = [Tile(self.start, "S")]
        current_pos = self.start
        next_pos = Pos(current_pos.x + start_directions[0], current_pos.y + start_directions[1])
        while next_pos != self.start:
            path.append(self.tiles[next_pos])
            next_pos, current_pos = self.tiles[next_pos].next(current_pos), next_pos

        from matplotlib.path import Path

        self.path = path
        self.mpl_path = Path([item.pos for item in path])
        return len(path) // 2

    # def __str__(self):
    #     repr = [ [self.tiles.get(Pos(i,j)).pipe if Pos(i,j) in self.tiles else '.' for i in range(self.shape[1])] for j in range(self.shape[0])]
    #     repr[self.start.y][self.start.x] = 'S'
    #     return '\n'.join(' '.join(line) for line in repr)

    # def waterfilled(self):
    #     ## Double size to get it to work
    #     shape = [item * 2 for item in self.shape]
    #     tiles = {}
    #     for j in range(shape[0]):
    #         for i in range(shape[1]):
    #             pos = Pos(i, j)
    #             if Pos(i//2 - 1, j//2) in self.tiles and self.tiles[Pos(i//2 - 1, j//2)].pipe == '-':
    #                 tiles[pos] = Tile(pos, '-')
    #             if Pos(i//2 + 1, j//2) in self.tiles and self.tiles[Pos(i//2 + 1, j//2)].pipe == '-':
    #                 tiles[pos] = Tile(pos, '-')
    #             if Pos(i//2, j//2 - 1) in self.tiles and self.tiles[Pos(i//2, j//2 - 1)].pipe == '|':
    #                 tiles[pos] = Tile(pos, '|')
    #             if Pos(i//2, j//2 + 1) in self.tiles and self.tiles[Pos(i//2, j//2 + 1)].pipe == '|':
    #                 tiles[pos] = Tile(pos, '|')
    #             if Pos(i//2, j//2) in self.tiles:
    #                 tiles[pos] = Tile(pos, self.tiles[Pos(i//2, j//2)].pipe)
    #     return Tiles(tiles, Pos(self.start.x * 2, self.start.x * 2), shape)

    def is_point_inside(self, pos: Pos) -> bool:
        # ray casting algorithm
        # assume points on (-1, pos.y) are outside the polygon
        # Count the number of crossing
        path = dict((tile.pos, tile) for tile in self.path)
        if pos in path:
            return False
        # tiles = self.tiles.copy()
        x_edges = [True for x in range(-1, pos.x) if Pos(x, pos.y) in path and path[Pos(x, pos.y)].pipe != "-"]
        y_edges = [True for y in range(-1, pos.y) if Pos(pos.x, y) in path and path[Pos(pos.x, y)].pipe != "|"]

        return bool(len(x_edges) % 2) and bool(len(y_edges) % 2)

    # def is_point_inside(self, pos: Pos) -> bool:
    #     if pos in self.path:
    #         return False
    #     return self.mpl_path.contains_point(pos)

    def enclosed(self):
        return sum([self.is_point_inside(Pos(i, j)) for j in range(self.shape[0]) for i in range(self.shape[1])])

    def __str__(self):
        repr = [
            [self.tiles.get(Pos(i, j)).pipe if Pos(i, j) in self.tiles else "." for i in range(self.shape[1])]
            for j in range(self.shape[0])
        ]
        repr[self.start.y][self.start.x] = "S"
        for j in range(self.shape[0]):
            for i in range(self.shape[1]):
                if self.is_point_inside(Pos(i, j)):
                    repr[j][i] = "I"
        return "\n".join(" ".join(line) for line in repr)

    @classmethod
    def parse_raw(cls, raw: str) -> "Tiles":
        tiles = {}
        start = None
        for j, line in enumerate(raw.split("\n")):
            for i, c in enumerate(line):
                pos = Pos(i, j)
                if c in ["|", "-", "L", "J", "7", "F"]:
                    tiles[pos] = Tile(pos, c)
                elif c == "S":
                    start = pos
                elif c in ["."]:
                    pass
                else:
                    raise ValueError(f"Unknown tile: {c}")
        shape = (j + 1, i + 1)
        return cls(tiles, start, shape)


RAW = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

TILES = Tiles.parse_raw(RAW)
assert TILES.explore_path() == 4

RAW = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

TILES = Tiles.parse_raw(RAW)
assert TILES.explore_path() == 8

RAW = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

TILES = Tiles.parse_raw(RAW)
TILES.explore_path()
assert TILES.enclosed() == 4

RAW = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""

TILES = Tiles.parse_raw(RAW)
TILES.explore_path()
assert TILES.enclosed() == 4

RAW = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

TILES = Tiles.parse_raw(RAW)
TILES.explore_path()
assert TILES.enclosed() == 8

with open("day10.txt", "r") as f:
    raw = f.read().strip()

tiles = Tiles.parse_raw(raw)
print(tiles.explore_path())  # 6800
print(tiles.enclosed())  # 483
