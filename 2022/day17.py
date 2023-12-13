from dataclasses import dataclass, field
from typing import List, Tuple, Iterator, Union
from itertools import cycle
from tqdm import trange


Point = Tuple[int, int]

"""
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

def rock_generator() -> Iterator[List[Point]]:
    while True:
        yield [(0, 0), (1, 0), (2, 0), (3,0)]
        yield [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
        yield [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        yield [(0, 0), (0, 1), (0, 2), (0, 3)]
        yield [(0, 0), (1, 0), (0, 1), (1, 1)]

@dataclass
class Rock:
    offsets: List[Point]
    bottom_left: Point

    @property
    def actual_position(self) -> List[Point]:
        return set([(item[0] + self.bottom_left[0], item[1] + self.bottom_left[1]) for item in self.offsets])

    def move(self, dx, dy):
        bottom_left = self.bottom_left[0] + dx, self.bottom_left[1] + dy
        return Rock(self.offsets, bottom_left)

@dataclass
class World:
    standing_rocks: set[Point] = field(repr=False, default_factory=lambda: set([(_, 0) for _ in range(8)]))
    highest_rock: int = 0

    def add_rock(self, rock: Rock):
        pts = rock.actual_position
        self.standing_rocks.update(pts)
        self.highest_rock = max([self.highest_rock ] + [y for _, y in pts])

    def show(self):
        repr = [list("." * 9) for _ in range(self.highest_rock+1) ]
        for pos in self.standing_rocks:
            repr[pos[1]][pos[0]] = "#"

        # walls
        for _ in range(8):
            repr[0][_] = "-"
        for _ in range(self.highest_rock+1):
            repr[_][0] = "|"
            repr[_][-1] = "|"
        repr[0][0] = repr[0][-1] = "+"

        print('\n'.join(reversed(["".join(item) for item in repr])))

@dataclass
class World2:
    floor: list = field(default_factory=lambda: [0] * 7)
    highest_rock: int = 0

    def add_rock(self, rock: Rock):
        pts = rock.actual_position
        for i in range(7):
            self.floor[i] = max([self.floor[i]] + [y for x, y in pts if (x - 1) == i])

        self.highest_rock = max([self.highest_rock ] + [y for _, y in pts])

    @property
    def standing_rocks(self):
        return set([(i+1, self.floor[i]) for i in range(7)])

    def show(self):
        repr = [list("." * 9) for _ in range(self.highest_rock+1) ]
        for pos in self.standing_rocks:
            repr[pos[1]][pos[0]] = "#"

        # walls
        for _ in range(8):
            repr[0][_] = "-"
        for _ in range(self.highest_rock+1):
            repr[_][0] = "|"
            repr[_][-1] = "|"
        repr[0][0] = repr[0][-1] = "+"

        print('\n'.join(reversed(["".join(item) for item in repr])))

@dataclass
class World3:
    standing_rocks: set[Point] = field(repr=False, default_factory=lambda: set([(_, 0) for _ in range(1, 8)]))
    highest_rock: int = 0
    line_list: List[Tuple[int, int]] = field(init=False, default_factory=list, repr=False)
    rock_counter: int = 0

    def add_rock(self, rock: Rock):
        pts = rock.actual_position
        self.standing_rocks.update(pts)
        self.highest_rock = max([self.highest_rock ] + [y for _, y in pts])

        self.rock_counter += 1

        # if a line is created remove everything below it
        line = []
        for _, y in pts:
            if all((x, y) in self.standing_rocks for x in range(1, 8)):
                line.append(y)
        if line:
            print('line found {}!'.format(len(line)))
            h = max(line)
            self.standing_rocks = {(x, y) for x, y in self.standing_rocks if y > h-1}
            self.line_list.append((self.rock_counter, h))

    def show(self):
        repr = [list("." * 9) for _ in range(self.highest_rock+1) ]
        for pos in self.standing_rocks:
            repr[pos[1]][pos[0]] = "#"

        # walls
        for _ in range(8):
            repr[0][_] = "-"
        for _ in range(self.highest_rock+1):
            repr[_][0] = "|"
            repr[_][-1] = "|"
        repr[0][0] = repr[0][-1] = "+"

        print('\n'.join(reversed(["".join(item) for item in repr])))


@dataclass
class Simulation:
    world: Union[World, World2]
    jet_pattern: str
    jet: Iterator = field(default_factory=lambda: None, repr=False)
    rock_generator: Iterator = field(default_factory=rock_generator, repr=False)

    def __post_init__(self):
        self.jet = cycle(self.jet_pattern)

    def rock_fall(self):
        shape = next(self.rock_generator)
        pos = (3, self.world.highest_rock+4)
        rock = Rock(shape, pos)
        while True:
            mouv = next(self.jet)
            match mouv:
                case '>':
                    dx = +1
                case '<':
                    dx = -1
                case _:
                    raise ValueError

            moved_rock = rock.move(dx, 0) 

            pts = moved_rock.actual_position
            if any(x < 1 for x,_ in pts) or any(x >= 8 for x,_ in pts) or pts & self.world.standing_rocks:
                pass
            else:
                rock = moved_rock

            moved_rock = rock.move(0, -1) 
            pts = moved_rock.actual_position 
            if pts & self.world.standing_rocks:
                break
            else:
                rock = moved_rock
            
        self.world.add_rock(rock)

    def run(self, iterations:int=2022) -> int:
        for _ in trange(iterations):
            self.rock_fall()

        return self.world.highest_rock


RAW=""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""


assert Simulation(World(), RAW).run() == 3068
# assert Simulation(World(), RAW).run(iterations=1000000000000) == 1514285714288

with open('day17.txt') as f:
    raw = f.read()
# print(Simulation(World(), raw).run())
# print(Simulation(World(), raw).run(iterations=1000000000000))

