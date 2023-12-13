from __future__ import annotations

from typing import List, Set, NamedTuple
from dataclasses import dataclass, field

RAW="""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

class Instruction(NamedTuple):
    op: str
    arg: int

    @staticmethod
    def from_line(line: str) -> Instruction:
        op, arg = line.strip().split()
        return Instruction(op, int(arg))

INSTRUCTIONS = [Instruction.from_line(line) for line in RAW.split('\n')]

@dataclass
class Isolation(object):
    bootcode: List[Instruction]
    index: int = 0
    accumulator: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        op, value = self.bootcode[self.index]

        if op == 'acc':
            self.accumulator += value
            self.index += 1
        elif op == 'jmp':
            self.index += value
        elif op == 'nop':
            self.index += 1
        else:
            raise ValueError(f'Unknown op{op}')

        if self.index == len(self.bootcode):
            raise StopIteration

    def iterate_until_repeat(self):
        visited = set()
        self.index = 0
        while self.index not in visited:
            visited.add(self.index)
            self.__next__()
        return self.accumulator


assert Isolation(INSTRUCTIONS).iterate_until_repeat() == 5

with open('day09.txt') as f:
    raw = f.read().strip()
    instructions = [Instruction.from_line(line) for line in raw.split('\n')]
    prog = Isolation(instructions)
    print(prog.iterate_until_repeat())



CORRECT="""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
nop -4
acc +6"""

def correct_bootcode(bootcode: List[Instruction]) -> int:

    # Brute force

    for i, (op, arg) in enumerate(bootcode):
        code = bootcode[:]
        if op == 'jmp':
            code[i] = Instruction("nop", arg)
        elif op == 'nop':
            code[i] = Instruction('jmp', arg)
        else:
            continue

        prog = Isolation(code)
        try:
            prog.iterate_until_repeat()
        except StopIteration:
            return prog.accumulator

assert correct_bootcode(INSTRUCTIONS) == 8
print(correct_bootcode(instructions))