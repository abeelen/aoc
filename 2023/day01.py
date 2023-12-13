RAW = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


"""
def parse_input(raw):
    numbers = []
    for line in raw.split('\n'):
        digits =  [item for item in line if item.isdigit()]
        numbers.append(int(digits[0]+digits[-1]))
    return sum(numbers)

with open('day01.txt', 'r') as f:
    raw = f.read().strip()

assert parse_input(RAW) == 142
print(parse_input(raw))
"""


def calibrate_line(line: str) -> int:
    digits = [int(item) for item in line if item.isdigit()]
    return 10 * digits[0] + digits[-1]


assert sum([calibrate_line(line) for line in RAW.split("\n")]) == 142

with open("day01.txt", "r") as f:
    raw = f.read().splitlines()

print(sum([calibrate_line(line) for line in raw]))

RAW = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

digits_dict = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

"""
def parse_input2(raw):
    numbers = []
    for line in raw.split('\n'):
        digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(c)
            else:
                for digit, value in digits_dict.items():
                    if line[i:].startswith(digit):
                        digits.append(value)
                
        numbers.append(int(digits[0]+digits[-1]))
    return sum(numbers)

assert parse_input2(RAW) == 281

print(parse_input2(raw))
"""


def calibrate_line2(line: str) -> int:
    digits = []
    for i, c in enumerate(line):
        if c.isdigit():
            digits.append(int(c))
        else:
            for digit, value in digits_dict.items():
                if line[i:].startswith(digit):
                    digits.append(int(value))

    return 10 * digits[0] + digits[-1]


assert sum([calibrate_line2(line) for line in RAW.split("\n")]) == 281
print(sum([calibrate_line2(line) for line in raw]))
