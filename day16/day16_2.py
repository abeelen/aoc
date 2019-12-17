from typing import List
from itertools import repeat, chain, cycle

def parse_input(raw: str) -> List[int]:
    return [int(i) for i in raw]

def print_output(output: List[int], offset: int=0, length: int=8)-> str:
    print(''.join([str(i) for i in output[offset:offset+length]]))

def parse_offset(input_value: List[int]) -> int:
    return int(''.join([str(i) for i in input_value[0:7]]))

def one_digit(n: int) -> int:
    return abs(n) % 10

def FFT(input_value: List[int], pattern: List[int]) -> List[int]:
 
    length = len(input_value)
    output = []
    for pos in range(1, length+1):
        coeffs = cycle(list(chain(*[repeat(coeff, pos) for coeff in pattern])))
        # Skip the first
        _ = next(coeffs)

        value = sum([value * coeff for value, coeff in zip(input_value, coeffs)])
        # Only keep last digit
        digit = one_digit(value) # int(str(value)[-1])
        output.append(digit)
    return output

def phase_FFT(input_value: List[int], pattern: List[int], phases: int) -> List[int]:

    output = input_value[:]
    for phase in range(phases):
        output = FFT(output, pattern)
    return output

with open('input') as f:
    raw = f.readline().strip()

# result = phase_FFT(parse_input(raw), PATTERN, 100)
# print_output(result, offset=0)

# PHASE 2

def part2(input_value: List[int], pattern: List[int]) -> str:

    numbers = input_value * 10_000
    offset = parse_offset(input_value)

    # That is inplace summation
    assert offset > len(numbers) // 2
    assert pattern[0] == 0

    for _ in range(100):

        # last position
        pos = len(numbers) - 1
        total = 0

        while pos >= offset:
            total += numbers[pos]
            numbers[pos] = one_digit(total)
            pos -= 1

    return numbers[offset:offset+8]

PATTERN=[0, 1, 0, -1]

#assert part2(parse_input("03036732577212944063491565474664"), PATTERN) == [8, 4, 4, 6, 2, 0, 2, 6]
#assert part2(parse_input("02935109699940807407585447034323"), PATTERN) == [7, 8, 7, 2, 5, 2, 7, 0]
#assert part2(parse_input("03081770884921959731165446850517"), PATTERN) == parse_input("53553731")

result = part2(parse_input(raw), PATTERN)
print_output(result)