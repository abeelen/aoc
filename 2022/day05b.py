from dataclasses import dataclass
import re


Stack = list[str]
Stacks = dict[int, Stack]

@dataclass
class Move:
    quantity: int
    from_: int
    to: int

@dataclass
class Problem:
    stacks: Stacks
    moves: list[Move]

    def move(self, move: Move) -> None:
        for _ in range(move.quantity):
            self.stacks[move.to].append(self.stacks[move.from_].pop())
    def move9001(self, move: Move) -> None:
        to_move = self.stacks[move.from_][-move.quantity:]
        self.stacks[move.from_] = self.stacks[move.from_][:-move.quantity]
        self.stacks[move.to] += to_move

    def run(self, model: int = 9000) -> None:
        for move in self.moves:
            if model == 9000:
                self.move(move)
            elif model == 9001:
                self.move9001(move)
            else:
                raise ValueError('Invalid model')

    @classmethod
    def parse_raw(cls, raw: str) -> 'Problem':
        stacks, moves = raw.split('\n\n')
        return cls(get_stacks(stacks), get_moves(moves))

def get_moves(raw: str) -> list[Move]:
    MOVE_REGEX='move ([0-9]+) from ([0-9]+) to ([0-9]+)'
    return [Move(*[int(i) for i in row]) for row in re.findall(MOVE_REGEX, raw)]

def get_stacks(raw: str) -> Stacks:

    lines = list(reversed(raw.splitlines()))
    cols = {int(c): i for i, c in enumerate(lines[0]) if c != " "}
    stacks = {
        c: [line[i] for line in lines[1:] if line[i] != " "]
        for c, i in cols.items()
    }
    return stacks

def get_top_stacks(stacks: Stacks)->str:
    return ''.join(item[-1] for item in stacks.values())

RAW="""    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

PROBLEM = Problem.parse_raw(RAW)
PROBLEM.run()

assert get_top_stacks(PROBLEM.stacks) == 'CMZ'

PROBLEM = Problem.parse_raw(RAW)
PROBLEM.run(model=9001)
assert get_top_stacks(PROBLEM.stacks) == 'MCD'

with open('day05.txt', 'r') as f:
    lines = f.read()

problem = Problem.parse_raw(lines)
problem.run()
print(get_top_stacks(problem.stacks))

problem = Problem.parse_raw(lines)
problem.run(model=9001)
print(get_top_stacks(problem.stacks))
