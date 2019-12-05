from typing import List, Tuple

Program = List[int]

def instruction_to_opcodemode(instruction: int) -> Tuple[int]:
    digits = [i for i in str(instruction).zfill(5)]
    opcode = int(''.join(digits[3:]))
    modes = [int(i) for i in reversed(digits[0:3])]
    return opcode, modes

def get_value(program: Program, ptr: int, mode: int) -> int:

    if mode == 0:
        addr = program[ptr]
        value = program[addr]
    elif mode ==1:
        value = program[ptr]
    else:
        raise ValueError("Unknown mode {}".format(mode))
    return value

def run(program: Program, _input: int=None) -> Program:
    ptr = 0
    output = []
    program = program[:]
    while program[ptr] != 99:

        opcode, modes = instruction_to_opcodemode(program[ptr])
        # print("program :", program)
        # print("opcode : ",opcode, "modes: ", modes)

        if opcode == 1: # +
            value1 = get_value(program, ptr+1, modes[0])
            value2 = get_value(program, ptr+2, modes[1])
            addr3 = program[ptr+3]
            program[addr3] = value1 + value2
            # print("value1: ", value1, "value2: ", value2, "value3: ", value1 + value2, "addr3: ", addr3)
            ptr += 4
        elif opcode == 2: # *
            value1 = get_value(program, ptr+1, modes[0])
            value2 = get_value(program, ptr+2, modes[1])
            addr3 = program[ptr+3] 
            # print("value1: ", value1, "value2: ", value2, "value3: ", value1 * value2, "addr3: ", addr3)
            program[addr3] = value1 * value2
            ptr += 4
        elif opcode == 3: # input
            addr = program[ptr+1]
            program[addr] = _input
            ptr += 2
        elif opcode == 4: # output
            # print("instruction: ",program[ptr:ptr+2])
            value = get_value(program, ptr+1, modes[0])
            # print("value: ", value)
            output.append(value)
            ptr += 2
        elif opcode == 5: # jump-if-true
            value1 = get_value(program, ptr+1, modes[0])
            value2 = get_value(program, ptr+2, modes[1])
            if value1 != 0:
                ptr = value2
            else:
                ptr += 3
        elif opcode == 6: # jump-if-false
            value1 = get_value(program, ptr+1, modes[0])
            value2 = get_value(program, ptr+2, modes[1])
            if value1 == 0:
                ptr = value2
            else:
                ptr += 3
        elif opcode == 7: # less than
            value1 = get_value(program, ptr+1, modes[0])
            value2 = get_value(program, ptr+2, modes[1])
            addr3 = program[ptr+3] 
            if value1 < value2:
                program[addr3] = 1
            else:
                program[addr3] = 0     
            ptr += 4
        elif opcode == 8: # equals
            value1 = get_value(program, ptr+1, modes[0])
            value2 = get_value(program, ptr+2, modes[1])
            addr3 = program[ptr+3] 
            if value1 == value2:
                program[addr3] = 1
            else:
                program[addr3] = 0     
            ptr += 4
        else:
            raise ValueError("Wrong opcode {}".format(opcode))

    return program, output

assert(run([3,9,8,9,10,9,4,9,99,-1,8], 8)[1] == [1])
assert(run([3,9,7,9,10,9,4,9,99,-1,8], 7)[1] == [1])
assert(run([3,9,7,9,10,9,4,9,99,-1,8], 8)[1] == [0])
assert(run([3,9,7,9,10,9,4,9,99,-1,8], 9)[1] == [0])
assert(run([3,3,1108,-1,8,3,4,3,99], 8)[1] == [1])
assert(run([3,3,1108,-1,8,3,4,3,99], 7)[1] == [0])
assert(run([3,3,1107,-1,8,3,4,3,99], 7)[1] == [1])
assert(run([3,3,1107,-1,8,3,4,3,99], 8)[1] == [0])

program = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1, 9]
assert(run(program, 0)[1] == [0])
assert(run(program, 1)[1] == [1])
program = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
assert(run(program, 0)[1] == [0])
assert(run(program, 1)[1] == [1])

program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
           1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
            999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
assert(run(program, 7)[1] == [999])
assert(run(program, 8)[1] == [1000])
assert(run(program, 9)[1] == [1001])


INPUT = 5

with open('input') as f:
    PROGRAM = [int(code) for code in f.readline().strip().split(',')]

prog, outputs  = run(PROGRAM, INPUT)