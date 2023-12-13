from dataclasses import dataclass, field, InitVar
from typing import Tuple

@dataclass
class Position:
    x: int = 0
    y: int = 0

def sign(n):
    if n==0:
        return 0
    elif n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        raise ValueError('n: %', str(n))

@dataclass
class Rope:
    head: Position = field(default_factory=Position)
    tail: Position = field(default_factory=Position)
    trail: set[Tuple] = field(default_factory=set)

    def print_trail(self, ncols=5, nrows = 6):
        board = [ ['.'] * 6 for _ in range(5)]

        for x,y in list(self.trail):
            board[y][x] = '#'

        print('\n'.join(reversed([''.join(row) for row in board])))

    def update_tail(self):
        dx = self.head.x - self.tail.x
        dy = self.head.y - self.tail.y
        if abs(dx) <= 1 and abs(dy) <= 1:
            return
        else:
            self.tail.x += sign(dx)
            self.tail.y += sign(dy)

        # if abs(dx) + abs(dy) > 2:
        #     if abs(dx) > 1:
        #         self.tail.x += dx // 2
        #     else: 
        #         self.tail.x += dx
        #     if abs(dy) > 1:
        #         self.tail.y += dy // 2
        #     else:
        #         self.tail.y += dy
        # elif abs(dx) > 1:
        #     self.tail.x += dx // 2
        # elif abs(dy) > 1:
        #     self.tail.y += dy // 2

        self.trail.add((self.tail.x, self.tail.y))   

    def run(self, commands: str) -> None:
        self.trail.add((0, 0))
        for command in commands.splitlines():
            direction, steps = command.split(' ')
            for _ in range(int(steps)):
                match direction:
                    case "R":
                        self.head.x += 1
                    case "U":
                        self.head.y += 1
                    case "L":
                        self.head.x -= 1
                    case "D":
                        self.head.y -= 1
                self.update_tail()


@dataclass
class Whip:
    n_knots: int = 10
    trail: set[Position] = field(default_factory=set)
    knots: InitVar[list[Position]] = None

    def __post_init__(self, knots):
        self.knots = []
        for _ in range(self.n_knots):
            self.knots.append(Position(0, 0))

    def print_trail(self, ncols=5, nrows = 6):
        board = [ ['.'] * 6 for _ in range(5)]

        for i, (x, y) in enumerate(self.trail):
            if i == 0:
                i = 'H'
            board[y][x] = str(i)

        print('\n'.join(reversed([''.join(row) for row in board])))

    def update_knots(self):
        for head, tail in zip(self.knots, self.knots[1:]):
            dx = head.x - tail.x
            dy = head.y - tail.y
            if abs(dx) <= 1 and abs(dy) <= 1:
                return
            else:
                tail.x += sign(dx)
                tail.y += sign(dy)
                        
        self.trail.add((self.knots[-1].x, self.knots[-1].y))   

    def run(self, commands: str) -> None:
        self.trail.add((0, 0))
        for command in commands.splitlines():
            direction, steps = command.split(' ')
            for _ in range(int(steps)):
                match direction:
                    case "R":
                        self.knots[0].x += 1
                    case "U":
                        self.knots[0].y += 1
                    case "L":
                        self.knots[0].x -= 1
                    case "D":
                        self.knots[0].y -= 1
                self.update_knots()

RAW = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST = Rope()
TEST.run(RAW)
assert len(TEST.trail) == 13

rope = Rope()
with open('day09.txt') as f:
    commands = f.read()

rope.run(commands)
print(len(rope.trail))

RAW = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
WHIP = Whip()
WHIP.run(RAW)
assert len(WHIP.trail) == 36

whip = Whip()
whip.run(commands)
print(len(whip.trail))