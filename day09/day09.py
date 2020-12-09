from typing import List
from dataclasses import dataclass

@dataclass
class XMAS:
    preamble: List[int]

    def is_valid(self, number: int)-> bool:
        for item in self.preamble:
            if number-item in self.preamble:
                return True
        return False
    
    def insert(self, number: int):
        if self.is_valid(number):
            self.preamble.pop(0)
            self.preamble.append(number)
        else:
            raise ValueError(f'{number} is not valid')

    def test(self, instructions: List[int]) -> int:
        for number in instructions:
            if self.is_valid(number):
                self.preamble.pop(0)
                self.preamble.append(number)
            else:
                return number

def find_bug(raw: str, length: int)-> int:
    numbers = [int(number) for number in raw.strip().split('\n')]
    preamble = numbers[0:length]
    to_test = numbers[length:]
    xmas = XMAS(preamble)
    return xmas.test(to_test)

RAW="""35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

assert find_bug(RAW, 5) == 127

with open('day09.txt') as f:
    raw = f.read()
    print(find_bug(raw, 25))

def find_contiguous_list(instructions: List[int], number: int):

    length = len(instructions)

    for i in range(0, length):
        for j in range(i+1, length):
            total = sum(instructions[i:j])
            if total == number:
                return instructions[i:j]
            if total > number:
                break

def encryption_weakness(raw: str, length: int)->int:
    instructions = [int(number) for number in raw.strip().split('\n')]
    preamble = instructions[0:length]
    to_test = instructions[length:]
    xmas = XMAS(preamble)
    number = xmas.test(to_test)

    contiguous = find_contiguous_list(instructions, number)
    return sum([min(contiguous), max(contiguous)])

assert encryption_weakness(RAW, 5) == 62

print(encryption_weakness(raw, 25))