from typing import List

INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

type Report = List[int]


def parse_input(input: str) -> List[Report]:
    lines = input.split("\n")
    return [list(map(int, line.split(" "))) for line in lines]


def is_safe(report: Report) -> bool:
    increasing = all([l > r for l, r in zip(report[0:-1], report[1:])])
    decreasing = all([l < r for l, r in zip(report[0:-1], report[1:])])
    good_diff = all([abs(l - r) > 0 and abs(l - r) < 4 for l, r in zip(report[0:-1], report[1:])])
    return (increasing or decreasing) and good_diff


def is_tolerable(report: Report) -> bool:
    if is_safe(report):
        return True

    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1 :]):
            return True

    return False


def how_much_safe(reports: List[Report]):
    return sum([is_safe(report) for report in reports])


def how_much_tolerable(reports: List[Report]):
    return sum([is_tolerable(report) for report in reports])


assert list(map(is_safe, parse_input(INPUT))) == [True, False, False, False, False, True]
assert how_much_safe(parse_input(INPUT)) == 2
assert how_much_tolerable(parse_input(INPUT)) == 4

with open("day02.txt", "r") as f:
    data = f.read()

print(how_much_safe(parse_input(data)))
print(how_much_tolerable(parse_input(data)))
