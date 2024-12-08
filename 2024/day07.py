from collections import namedtuple
from functools import reduce
from itertools import product
from operator import add, mul
from typing import List

RAW_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


Equation = namedtuple("Equation", ["result", "values"])


# DAAAAAAAAAAAAAAAAAAAAAAAAAM, dict was a bad idea...
def parse_input(raw_input: str) -> List[Equation]:
    return [
        Equation(int(k), list(map(int, v.split())))
        for k, v in (line.split(": ") for line in raw_input.strip().split("\n"))
    ]


def check(result: int, values: List[int], ops=(add, mul)) -> List[int]:
    # Brute force all possible operations
    all_operators = product(ops, repeat=len(values) - 1)
    for operators in all_operators:
        if (
            reduce(
                lambda ops, val: val[0](ops, val[1]),
                zip(operators, values[1:]),
                values[0],
            )
            == result
        ):
            return True

    return False


def total_calibration_result(data: List[Equation], ops=(add, mul)) -> int:
    return sum([result for result, values in data if check(result, values, ops=ops)])


assert total_calibration_result(parse_input(RAW_INPUT)) == 3749


with open("day07.txt") as f:
    raw_input = f.read().strip()
# print(total_calibration_result(parse_input(raw_input)))


def concat(a, b):
    return int(str(a) + str(b))


# %timeit concat(15, 6)
# 672 ns ± 57.7 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)


def concat(a, b):
    return int(f"{a}{b}")


# %timeit concat(15, 6)
# 608 ns ± 29.6 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)


def concat(a, b):
    return a * 10 ** len(str(b)) + b


# %timeit concat(15, 6)
# 298 ns ± 7.89 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)


assert concat(15, 6) == 156
assert total_calibration_result(parse_input(RAW_INPUT), ops=(add, mul, concat)) == 11387
print(total_calibration_result(parse_input(raw_input), ops=(add, mul, concat)))
