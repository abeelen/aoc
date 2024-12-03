from typing import List, Tuple
from collections import Counter

INPUT = """3   4
4   3
2   5
1   3
3   9
3   3"""


def parse_input(input: str) -> Tuple[List[int], List[int]]:
    left = []
    right = []
    for line in input.strip().split("\n"):
        l, r = line.split()
        left.append(int(l))
        right.append(int(r))
    return left, right


def calculate_distance(L: List[int], R: List[int]) -> int:
    L.sort()
    R.sort()
    return sum([abs(l - r) for l, r in zip(L, R)])


def similarity_score(L: List[int], R: List[int]) -> int:
    cl = Counter(L)
    cr = Counter(R)
    sr = set(R)
    sl = set(L)
    return sum([k * cr[k] for k in L if k in sr]) 


assert calculate_distance(*parse_input(INPUT)) == 11
assert similarity_score(*parse_input(INPUT)) == 31

with open("day01.txt", "r") as f:
    data = f.read()

print(calculate_distance(*parse_input(data)))
print(similarity_score(*parse_input(data)))
