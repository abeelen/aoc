from typing import List

def cpu(raw: str, output_cycle: List[int] = [20, 60, 100, 140, 180, 220]) -> List[int]:
    register = 1
    registers = [1]

    for instruction in raw.splitlines():
        match instruction.split():
            case ["noop"]:
                registers.append(register)
            case ["addx", amount]:
                registers.append(register)
                register += int(amount)
                registers.append(register)

    return sum([cycle * registers[cycle-1] for cycle in output_cycle])


def draw(raw: str) -> List[int]:
    register = 1
    registers = [1]

    for instruction in raw.splitlines():
        match instruction.split():
            case ["noop"]:
                registers.append(register)
            case ["addx", amount]:
                registers.append(register)
                register += int(amount)
                registers.append(register)

    CRTS = []
    CRT = ""
    for cycle, register in enumerate(registers):
        cycle = cycle % 40
        register -= 1
        if cycle == 0:
            CRTS.append(CRT)
            CRT = ""
        if register <= cycle  <= register + 2:
            CRT += "#"
        else:
            CRT += '.'
    print('\n'.join(CRTS))

RAW="""addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

assert cpu(RAW) == 13140

with open('day10.txt') as f:
    raw = f.read()

print(cpu(raw))
draw(raw)