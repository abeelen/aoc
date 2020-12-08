from typing import List
from dataclasses import dataclass, field

@dataclass
class Isolation(object):
    bootcode: List[str]
    index: int = 0
    accumulator: int = 0
    visited: List[int] = field(default_factory=list[int])

    def __iter__(self):
        return self

    def __next__(self):
        self.visited.append(self.index)
        instr, value = self.bootcode[self.index].split()

        if instr == 'acc':
            self.accumulator += int(value)
            self.index += 1
        elif instr == 'jmp':
            self.index += int(value)
        elif instr == 'nop':
            self.index += 1
        else:
            raise ValueError('Unknown instruction')

        if self.index == len(self.bootcode):
            raise StopIteration
        
        if self.index in self.visited:
            raise ValueError

RAW="""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

with open('day09.txt') as f:
    raw = f.read().strip()

prog = Isolation(raw.split('\n'))


try:
    _ = list(prog)
except ValueError:
    print(prog.accumulator)


CORRECT="""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
nop -4
acc +6"""

def correct_bootcode(bootcode: List[str]):

    # Brute force
    index = 0
    while index < len(bootcode):
        instr, value = bootcode[index].split()
        if instr not in ['jmp', 'nop']:
            index +=1
            continue

        code = bootcode.copy()
        if instr == 'jmp':
            code[index] = f"nop {value}"
        elif instr == 'nop':
            code[index] = f'jmp {value}'

        prog = Isolation(code)
        try:
            _ = list(prog)
            break
        except ValueError:
            index += 1
    
    print(prog.accumulator)

correct_bootcode(raw.split('\n'))