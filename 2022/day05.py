from collections import deque
import re

RE = re.compile('move ([0-9]+) from ([0-9]+) to ([0-9]+)')


def parse_stacks(stack_lines):
    lines = stack_lines.split('\n')
    n_stacks = (len(lines[0]) + 1) // 4
    
    stacks = [deque() for _ in range(n_stacks)]
    for line in lines[:-1]:
        for item, stack in zip(line[1::4], stacks):
            if item != ' ':
                stack.appendleft(item)

    return stacks

def run_instructions(instr_lines, stacks):
    lines = instr_lines.strip().split('\n')
    for line in lines:
        number, i_from, i_to = RE.match(line).groups()
        number = int(number)
        i_from = int(i_from) - 1
        i_to = int(i_to) - 1
        for _ in range(0, int(number)):
            stacks[i_to].append(stacks[i_from].pop())
    return ''.join([stack[-1] for stack in stacks])

def run_instructions_cm9001(instr_lines, stacks):
    lines = instr_lines.strip().split('\n')
    for line in lines:
        number, i_from, i_to = RE.match(line).groups()
        number = int(number)
        i_from = int(i_from) - 1
        i_to = int(i_to) - 1
        intermediate = deque()
        for _ in range(0, number):
            intermediate.append(stacks[i_from].pop())
        for _ in range(0, number):
            stacks[i_to].append(intermediate.pop())
    return ''.join([stack[-1] for stack in stacks])

def run(lines):
    stacks_line, instr_lines = lines.split('\n\n')
    stacks = parse_stacks(stacks_line)
    return run_instructions(instr_lines, stacks)

def run_cm9001(lines):
    stacks_line, instr_lines = lines.split('\n\n')
    stacks = parse_stacks(stacks_line)
    return run_instructions_cm9001(instr_lines, stacks)


RAW="""    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

assert run(RAW) == 'CMZ'

assert run_cm9001(RAW) == 'MCD'

with open('day05.txt', 'r') as f:
    lines = f.read()

print(run(lines))
print(run_cm9001(lines))