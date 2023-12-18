from dataclasses import dataclass, field
from typing import Set, List, Dict, NamedTuple, Tuple

RAW = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


class Pos(NamedTuple):
    x: int
    y: int


Dir = Pos


class Ray(NamedTuple):
    pos: Pos
    dir: Dir


@dataclass
class Grid:
    tiles: Dict[Pos, str]
    shape: Tuple[int, int]
    rays: List[Ray] = field(default_factory=list)
    rays_history: set[Ray] = field(default_factory=set)
    energised: set[Pos] = field(default_factory=set)

    def __str__tiles__(self):
        output = []
        for y in range(self.shape[0] + 1):
            line = []
            for x in range(self.shape[1] + 1):
                pos = Pos(x, y)
                if pos not in self.tiles:
                    line.append(".")
                else:
                    line.append(self.tiles[pos])
            output.append("".join(line))
        tiles = "\n".join(output)
        return tiles

    def __str__energised__(self):
        if self.energised:
            output = [
                "".join(["#" if Pos(x, y) in self.energised else "." for x in range(self.shape[1] + 1)])
                for y in range(self.shape[0] + 1)
            ]
            energised = "\n".join(output)
        else:
            energised = ""
        return energised

    def __str__(self) -> str:
        tiles = self.__str__tiles()
        energised = self.__str__energised__()
        return "\n\n".join([tiles, energised])

    def step(self) -> None:
        rays: List[Ray] = []
        for ray in self.rays:
            if ray in self.rays_history:
                continue

            self.rays_history.add(ray)

            x = ray.pos.x + ray.dir.x
            y = ray.pos.y + ray.dir.y

            if 0 > x or x > self.shape[1] or 0 > y or y > self.shape[0]:
                # ray is out of bounds
                continue
            pos = Pos(x, y)
            self.energised.add(pos)

            if pos not in self.tiles:
                rays.append(Ray(pos, ray.dir))
                continue
            elif self.tiles[pos] == "|" and abs(ray.dir.x) != 0:
                rays.append(Ray(pos, Dir(0, 1)))
                rays.append(Ray(pos, Dir(0, -1)))
            elif self.tiles[pos] == "-" and abs(ray.dir.y) != 0:
                rays.append(Ray(pos, Dir(1, 0)))
                rays.append(Ray(pos, Dir(-1, 0)))
            elif self.tiles[pos] == "\\":
                rays.append(Ray(pos, Dir(ray.dir.y, ray.dir.x)))
            elif self.tiles[pos] == "/":
                rays.append(Ray(pos, Dir(-ray.dir.y, -ray.dir.x)))
            else:
                rays.append(Ray(pos, ray.dir))
        self.rays = rays

    def run(self, start=Ray(Pos(-1, 0), Dir(1, 0))) -> None:
        self.rays = [start]
        self.energised = set()
        self.rays_history = set()
        while self.rays:
            self.step()
        return len(self.energised)

    def find_max_energize(self):
        energized = []
        energized += [self.run(start=Ray(Pos(-1, y), Dir(1, 0))) for y in range(self.shape[0] + 1)]
        energized += [self.run(start=Ray(Pos(self.shape[1] + 1, y), Dir(-1, 0))) for y in range(self.shape[0] + 1)]
        energized += [self.run(start=Ray(Pos(x, -1), Dir(0, 1))) for x in range(self.shape[1] + 1)]
        energized += [self.run(start=Ray(Pos(x, self.shape[0] + 1), Dir(0, -1))) for x in range(self.shape[1] + 1)]

        return max(energized)

    @classmethod
    def parse_raw(cls, raw: str) -> "Grid":
        tiles: Dict[Pos, str] = {}
        for y, line in enumerate(raw.split("\n")):
            for x, tile in enumerate(line):
                if tile != ".":
                    tiles[Pos(x, y)] = tile

        return cls(tiles, (y, x))


GRID = Grid.parse_raw(RAW)
assert Grid.parse_raw(RAW).run() == 46
assert Grid.parse_raw(RAW).find_max_energize() == 51


with open("day16.txt", "r") as f:
    raw = f.read().strip()

grid = Grid.parse_raw(raw)
print(grid.run())
print(grid.find_max_energize())
