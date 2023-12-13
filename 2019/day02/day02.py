from typing import List

Program = List[int]

def run(program: Program) -> Program:
    idx = 0
    while program[idx] != 99:

        opcode = program[idx]
        addr1, addr2, addr3 = program[idx+1], program[idx+2], program[idx+3]

        if opcode == 1: # +
            program[addr3] = program[addr1] + program[addr2]
        elif opcode == 2: # * 
            program[addr3] = program[addr1] * program[addr2]
        else:
            raise ValueError("Wrong opcode {}".format(opcode))

        idx += 4
    return program

assert run([1,0,0,0,99]) == [2,0,0,0,99]
assert run([2,3,0,3,99]) == [2,3,0,6,99]
assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

with open('input') as f:
    PROGRAM = [int(code) for code in f.readline().strip().split(',')]

def memory(PROGRAM, noun, verb):
    codes = PROGRAM[:]
    codes[1] = noun
    codes[2] = verb
    return run(codes)[0]

print(memory(PROGRAM, 12, 2))

from itertools import product
nouns = range(99)
verbs = range(99)

TARGET = 19690720

for noun, verb in product(nouns, verbs):
    if memory(PROGRAM, noun, verb) == TARGET:
        print(100 * noun + verb)
        break
