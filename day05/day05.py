from typing import List, Tuple

Program = List[int]

def instruction_to_opcodemode(instruction: int) -> Tuple[int]:
    digits = [i for i in str(instruction).zfill(5)]
    opcode = int(''.join(digits[3:]))
    modes = [int(i) for i in reversed(digits[0:3])]
    return opcode, modes

def get_value(program: Program, self.ptr: int, mode: int) -> int:

    if mode == 0:
        addr = program[self.ptr]
        value = program[addr]
    elif mode ==1:
        value = program[self.ptr]
    else:
        raise ValueError("Unknown mode {}".format(mode))
    return value

def run(program: Program, _input: int=None) -> Program:
    self.ptr = 0
    output = []
    while program[self.ptr] != 99:

        opcode, modes = instruction_to_opcodemode(program[self.ptr])
        # print("program :", program)
        # print("opcode : ",opcode, "modes: ", modes)

        if opcode == 1: # +
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            addr3 = program[self.ptr+3]
            program[addr3] = value1 + value2
            # print("value1: ", value1, "value2: ", value2, "value3: ", value1 + value2, "addr3: ", addr3)
            self.ptr += 4
        elif opcode == 2: # *
            value1 = get_value(program, self.ptr+1, modes[0])
            value2 = get_value(program, self.ptr+2, modes[1])
            addr3 = program[self.ptr+3] 
            # print("value1: ", value1, "value2: ", value2, "value3: ", value1 * value2, "addr3: ", addr3)
            program[addr3] = value1 * value2
            self.ptr += 4
        elif opcode == 3: # input
            addr = program[self.ptr+1]
            program[addr] = _input
            self.ptr += 2
        elif opcode == 4: # output
            # print("instruction: ",program[self.ptr:self.ptr+2])
            value = get_value(program, self.ptr+1, modes[0])
            # print("value: ", value)
            output.append(value)
            self.ptr += 2

        else:
            raise ValueError("Wrong opcode {}".format(opcode))

    return program, output

# assert(run([3,0,4,0,99], 2)[1] == [2])
# assert(run([1002,4,3,4,33])[0][-1] == 99)
# assert(run([1101,100,-1,4,0])[0][-1] == 99)

INPUT = 1

with open('input') as f:
    PROGRAM = [int(code) for code in f.readline().strip().split(',')]

prog, outputs  = run(PROGRAM, INPUT)