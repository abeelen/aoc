PASSWORD = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

import re

def validate(line: str) -> bool:
    cmin, cmax, char, password = re.match('(\d*)-(\d*) (.): (.*)', line).groups()
    c = password.count(char)
    return (int(cmin) <= c) & (c <= int(cmax))


assert [validate(line.strip()) for line in PASSWORD.split('\n')] == [True, False, True]

with open('day02.txt') as f:
    validation = [validate(line.strip()) for line in f]

print(sum(validation))

## Part Two
