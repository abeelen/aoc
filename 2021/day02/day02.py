INPUT="""forward 5
down 5
forward 8
up 3
down 8
forward 2"""

from math import prod

def parse_input(input):
    return [tuple(line.split(' ')) for line in input]


def run(commands, horizontal = 0, depth = 0):
    for command, value in commands:
        value = int(value)
        if command == 'forward':
            horizontal += value
        elif command == 'down':
            depth += value
        elif command == 'up':
            depth -= value
        else:
            raise ValueError('Unknown command : {}'.format(command))

    return horizontal, depth

assert prod(run(parse_input(INPUT.split('\n')))) == 150

with open('input.txt', 'r') as f:
    input = f.readlines()

print(prod(run(parse_input(input))))


def run2(commands, horizontal = 0, depth = 0, aim=0):
    for command, value in commands:
        value = int(value)
        if command == 'forward':
            horizontal += value
            depth += aim * value
        elif command == 'down':
            aim += value
        elif command == 'up':
            aim -= value
        else:
            raise ValueError('Unknown command : {}'.format(command))

    return horizontal, depth

assert prod(run2(parse_input(INPUT.split('\n')))) == 900
print(prod(run2(parse_input(input))))
