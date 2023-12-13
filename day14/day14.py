from dataclasses import dataclass, field
from typing import Dict
import re
from itertools import repeat, product

RAW = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""


def setBit(int_type, offset):
    mask = 1 << offset
    return int_type | mask


def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return int_type & mask


@dataclass
class Initialization:
    mask: str = None
    idxs_set: list = field(default_factory=list)
    idxs_clear: list = field(default_factory=list)
    memory: Dict = field(default_factory=dict)

    def parse_program(self, raw: str):
        lines = raw.strip().split("\n")
        for line in lines:
            self.run_line(line)

    def run_line(self, line: str):
        inst, value = line.strip().split(" = ")
        if inst == "mask":
            self.mask = value
            self.idxs_set = list(
                35 - i_set.start() for i_set in re.finditer("1", value)
            )
            self.idxs_clear = list(
                35 - i_set.start() for i_set in re.finditer("0", value)
            )
        elif inst[0:3] == "mem":
            idx = int(re.match("mem\[(\d*)\]", inst).groups()[0])
            value = int(value)
            for idx_set in self.idxs_set:
                value = setBit(value, idx_set)
            for idx_clear in self.idxs_clear:
                value = clearBit(value, idx_clear)
            self.memory[idx] = value

    def sum(self):
        return sum(self.memory.values())


prog = Initialization()
prog.parse_program(RAW)
assert prog.sum() == 165

with open("day14.txt") as f:
    raw = f.read()

prog = Initialization()
prog.parse_program(raw)
print(prog.sum())


def mad(raw: str):

    mask = None
    memory = dict()
    idxs_set = list()
    idxs_float = list()

    for line in raw.strip().split("\n"):
        inst, value = line.strip().split(" = ")
        if inst == "mask":
            mask = value
            idxs_set = list(35 - i_set.start() for i_set in re.finditer("1", value))
            idxs_float = list(35 - i_set.start() for i_set in re.finditer("X", value))
        elif inst[0:3] == "mem":
            idx = int(re.match("mem\[(\d*)\]", inst).groups()[0])
            value = int(value)

            for idx_set in idxs_set:
                idx = setBit(idx, idx_set)

            # Float values :
            for choices in product(*repeat([0, 1], len(idxs_float))):
                masked_idx = idx
                for choice, idx_float in zip(choices, idxs_float):
                    if choice == 0:
                        masked_idx = clearBit(masked_idx, idx_float)
                    elif choice == 1:
                        masked_idx = setBit(masked_idx, idx_float)
                memory[masked_idx] = value

    return sum(memory.values())


RAW2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

assert mad(RAW2) == 208

print(mad(raw))