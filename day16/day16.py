from typing import List
from itertools import repeat, chain, cycle

def parse_input(raw: str) -> List[int]:
    return [int(i) for i in raw]

def print_output(output: List[int], offset: int=0, length: int=8)-> str:
    print(''.join([str(i) for i in output[offset:offset+length]]))

def parse_offset(input_value: List[int]) -> int:
    return int(''.join([str(i) for i in input_value[0:7]]))

def FFT(input_value: List[int], pattern: List[int]) -> List[int]:
 
    length = len(input_value)
    output = []
    for pos in range(1, length+1):
        coeffs = cycle(list(chain(*[repeat(coeff, pos) for coeff in pattern])))
        # Skip the first
        _ = next(coeffs)

        value = sum([value * coeff for value, coeff in zip(input_value, coeffs)])
        # Only keep last digit
        digit = int(str(value)[-1])
        output.append(digit)
    return output

def phase_FFT(input_value: List[int], pattern: List[int], phases: int) -> List[int]:

    output = input_value[:]
    for phase in range(phases):
        output = FFT(output, pattern)
    return output

RAW=parse_input("12345678")
PATTERN=[0, 1, 0, -1]
assert FFT(RAW, PATTERN) == [4, 8, 2, 2, 6, 1, 5, 8]
assert phase_FFT(RAW, PATTERN, 2) == [3, 4, 0, 4, 0, 4, 3, 8]
assert phase_FFT(RAW, PATTERN, 4) == [0, 1, 0, 2, 9, 4, 9, 8]

RAW = parse_input("80871224585914546619083218645595")
assert phase_FFT(RAW, PATTERN, 100)[0:8] == parse_input("24176176")

RAW = parse_input("19617804207202209144916044189917")
assert phase_FFT(RAW, PATTERN, 100)[0:8] == parse_input("73745418")


with open('input') as f:
    raw = f.readline().strip()

result = phase_FFT(parse_input(raw), PATTERN, 100)
print_output(result, offset=0)
