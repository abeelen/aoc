from typing import List, Counter
from collections import Counter

RAW="""16
10
15
5
1
11
7
19
6
12
4"""

RAW2="""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

ADAPTORS = [int(number) for number in RAW.split('\n')]
ADAPTORS2 = [int(number) for number in RAW2.split('\n')]

def find_diff(numbers: List[int])->Counter[int]:
    numbers.append(0)
    numbers.append(max(numbers)+3)
    numbers.sort()
    c = Counter([i-j for i,j in zip(numbers[1:], numbers)])
    return c[3] * c[1]

def find_path(numbers: List[int])->int:
    numbers.append(0)
    numbers.append(max(numbers)+3)

    output = numbers[-1]
    n_path = [0] * (output + 1)
    n_path[0] = 1
    if 1 in numbers:
        n_path[1] = 1
    if 2 in numbers and 1 in numbers:
        n_path[2] = 2
    elif 2 in numbers:
        n_path[1] = 1

    for n in range(3, output+1):
        if n not in numbers:
            continue
        n_path[n] = n_path[n-1] + n_path[n-2] + n_path[n-3]

    return n_path[output]

assert find_diff(ADAPTORS) == 7 * 5
assert find_diff(ADAPTORS2) == 22 * 10

assert find_path(ADAPTORS) == 8
assert find_path(ADAPTORS2) == 19208

with open('day10.txt') as f:
    adaptors =[int(number) for number in f.read().strip().split('\n')]

    print(find_diff(adaptors))
    print(find_path(adaptors))