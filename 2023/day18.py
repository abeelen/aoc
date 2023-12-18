from dataclasses import dataclass
from typing import List, NamedTuple
from matplotlib.path import Path
from itertools import product
from tqdm import tqdm


RAW = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


class Pos(NamedTuple):
    x: int
    y: int


class Instruction(NamedTuple):
    direction: str
    meter: int
    color: str


@dataclass
class DigPlan:
    instructions: List[Instruction]

    def outline(self) -> List[Pos]:
        current: Pos = Pos(0, 0)
        outline: List[Pos] = []

        for direction, meter, _ in self.instructions:
            if direction == "R":
                outline += [Pos(current.x + dx, current.y) for dx in range(1, meter + 1)]
            elif direction == "L":
                outline += [Pos(current.x - dx, current.y) for dx in range(1, meter + 1)]
            elif direction == "U":
                outline += [Pos(current.x, current.y - dy) for dy in range(1, meter + 1)]
            elif direction == "D":
                outline += [Pos(current.x, current.y + dy) for dy in range(1, meter + 1)]

            current = outline[-1]

        return outline

    def outline_edges(self) -> List[Pos]:
        current: Pos = Pos(0, 0)
        outline: List[Pos] = [current]

        for direction, meter, _ in self.instructions:
            if direction == "R":
                outline.append(Pos(current.x + meter, current.y))
            elif direction == "L":
                outline.append(Pos(current.x - meter, current.y))
            elif direction == "U":
                outline.append(Pos(current.x, current.y - meter))
            elif direction == "D":
                outline.append(Pos(current.x, current.y + meter))

            current = outline[-1]

        return outline

    def swap_color(self) -> "DigPlan":
        instructions: List[Instruction] = []
        for _, _, color in self.instructions:
            if color[-1] == "0":
                direction = "R"
            elif color[-1] == "1":
                direction = "D"
            elif color[-1] == "2":
                direction = "L"
            elif color[-1] == "3":
                direction = "U"
            else:
                raise ValueError(f"Invalid diretion {color}")

            number = int(color[1:6], 16)

            instructions.append(Instruction(direction, number, color))
        return DigPlan(instructions)

    def fill_outline_brute(self) -> int:
        # Way too brutal for part 2....

        outline = self.outline()
        outline_edges = self.outline_edges()
        xs = [item.x for item in outline]
        ys = [item.y for item in outline]
        path = Path([item for item in outline_edges])

        points = list(product(range(min(xs), max(xs) + 1), range(min(ys), max(ys) + 1)))

        # inside = path.contains_points(points)
        # within_outline = [item in outline for item in points]
        # overall = [this or that for this, that in zip(inside, within_outline)]

        overall = [path.contains_point(Pos(x, y)) or Pos(x, y) in outline for x, y in tqdm(points, leave=False)]
        return sum(overall)

    def perimeter(self) -> int:
        return sum(item.meter for item in self.instructions)

    def fill_outline_gauss(self) -> int:
        outline_edges = self.outline_edges()

        outline_edges.append(outline_edges[0])
        # https://en.wikipedia.org/wiki/Shoelace_formula
        # Triangle formula
        A = [(pos_i.x * pos_j.y - pos_j.x * pos_i.y) for pos_i, pos_j in zip(outline_edges[:-1], outline_edges[1:])]
        A = abs(sum(A) // 2)
        # so A is the area
        # Pick's Theorem https://en.wikipedia.org/wiki/Pick%27s_theorem
        # A = i + b/2 + 1
        # A the area b the boundary points (perimeter)
        # i the points inside, A given by the shoelace formula
        # so i = A - b/2 + 1
        # so the total area is i + perimeter = A + b/2 + 1
        return A + self.perimeter() // 2 + 1

    @classmethod
    def parse_raw(cls, raw: str) -> "DigPlan":
        instructions: List[Instruction] = []
        for line in raw.split("\n"):
            direction, number, color = line.split(" ")
            number = int(number)
            color = color[1:-1]
            instructions.append(Instruction(direction, number, color))
        return cls(instructions)


DIGPLAN = DigPlan.parse_raw(RAW)
assert len(DIGPLAN.outline()) == 38
# assert DIGPLAN.fill_outline_brute() == 62
assert DIGPLAN.fill_outline_gauss() == 62
assert DIGPLAN.swap_color().fill_outline_gauss() == 952408144115

with open("day18.txt", "r") as f:
    raw = f.read().strip()

digplan = DigPlan.parse_raw(raw)
print(digplan.fill_outline_gauss())
print(digplan.swap_color().fill_outline_gauss())
