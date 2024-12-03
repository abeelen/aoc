import re

INPUT="""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

def multiply_some_number(data: str) -> int:
    results = []
    for op in re.finditer(r'mul\((\d+),(\d+)\)', data):
        numbers = list(map(int, op.groups()))
        results.append(numbers[0] * numbers[1])
    return sum(results)

assert multiply_some_number(INPUT) == 161

with open('day03.txt', 'r') as f:
    data = f.read()
    
print(multiply_some_number(data))

INPUT="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def multiply_some_number_if(data: str) -> int:
    results = []
    enabled = True
    for a, b, do, dont in re.findall(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", data):
        if do or dont:
            enabled = bool(do)
        else:
            if enabled:
                results.append(int(a) * int(b))
    return sum(results)

assert multiply_some_number_if(INPUT) == 48

print(multiply_some_number_if(data))