from typing import List

RAW = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def parse_raw(raw: str) -> List[List[int]]:
    return [[int(c) for c in line.split()] for line in raw.strip().split("\n")]


def predict_next(history: List[int]) -> int:
    derivatives = [n - p for n, p in zip(history[1:], history[:-1])]
    last_derivatives = [history[-1]]
    while not all([d == 0 for d in derivatives]):
        last_derivatives.append(derivatives[-1])
        derivatives = [n - p for n, p in zip(derivatives[1:], derivatives[:-1])]
    return sum(last_derivatives)


def predict_previous(history: List[int]) -> int:
    derivatives = [n - p for n, p in zip(history[1:], history[:-1])]
    first_derivatives = [history[0]]
    sign = -1
    while not all([d == 0 for d in derivatives]):
        first_derivatives.append(sign * derivatives[0])
        sign *= -1
        derivatives = [n - p for n, p in zip(derivatives[1:], derivatives[:-1])]
    return sum(first_derivatives)


SEQ = parse_raw(RAW)
assert [predict_next(H) for H in SEQ] == [18, 28, 68]
assert sum([predict_next(H) for H in SEQ]) == 114
assert [predict_previous(H) for H in SEQ] == [-3, 0, 5]
assert sum([predict_previous(H) for H in SEQ]) == 2

with open("day09.txt", "r") as f:
    raw = f.read().strip()

seq = parse_raw(raw)
print(sum([predict_next(h) for h in seq]))
print(sum([predict_previous(h) for h in seq]))
