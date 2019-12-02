
opcode = [1, 2, 99]

Intcode = [1,9,10,3,
           2,3,11,0,
           99,
           30,40,50]

def Intcode(code):
    idx = 0
    while idx < len(code):
        opcode = code[idx]

        if opcode == 99:
            return code

        if opcode not in [1, 2]:
            return code

        addr1, addr2, addr3 = [code[idx+i] for i in range(1, 4)]
        mem1 = code[addr1]
        mem2 = code[addr2]

        if code[idx] == 1:
            code[addr3] = mem1 + mem2
        elif code[idx] == 2:
            code[addr3] = mem1 * mem2
        idx += 4
    return code

assert Intcode([1,0,0,0,99]) == [2,0,0,0,99]
assert Intcode([2,3,0,3,99]) == [2,3,0,6,99]
assert Intcode([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert Intcode([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

with open('input') as f:
    codes = [int(code) for code in f.readline().strip().split(',')]

codes[1] = 12
codes[2] = 2
print(Intcode(codes)[0])

def memory(noun, verb):
    with open('input') as f:
        codes = [int(code) for code in f.readline().strip().split(',')]

    codes[1] = noun
    codes[2] = verb
    return Intcode(codes)[0]

from itertools import product
nouns = range(99)
verbs = range(99)

for noun, verb in product(nouns, verbs):
    if memory(noun, verb) == 19690720:
        print(100 * noun + verb)
