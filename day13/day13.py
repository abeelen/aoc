from typing import Tuple, List

RAW = """939
7,13,x,x,59,x,31,19"""


def parse_input(raw: str) -> Tuple[int, List[int]]:
    timestamp, buses = raw.strip().split("\n")
    timestamp = int(timestamp)
    buses = [int(bus) for bus in buses.split(",") if bus != "x"]
    return timestamp, buses


def closest_bus(timestamp: int, buses: List[int]) -> int:
    missed_by = [timestamp % bus for bus in buses]
    waits = {bus: bus - miss for bus, miss in zip(buses, missed_by) if miss > 0}

    bus = min(buses, key=lambda bus: waits[bus])

    return bus * waits[bus]


TIMESTAMP, IDS = parse_input(RAW)
assert closest_bus(*parse_input(RAW)) == 295

with open("day13.txt") as f:
    raw = f.read()
print(closest_bus(*parse_input(raw)))


# Crazy not working....
def brut_find(raw: str, start: int = 0) -> int:
    ids = [(i, int(id)) for i, id in enumerate(raw.strip().split(",")) if id != "x"]

    t = start
    while (t % ids[0][1] != 0) or (not all(t % id == id - i for i, id in ids[1:])):
        t += 1
    return t


# joelgruss


def make_factors(raw_buses: List[str]):
    indexed = [(i, int(bus)) for i, bus in enumerate(raw_buses) if bus != "x"]
    factors = [(bus, (bus - i) % bus) for i, bus in indexed]
    return factors


def chinese_remainder(divisors: List[int], remainders: List[int]) -> int:
    solution = remainders[0]
    increment = divisors[0]

    # invariant: at step i, we have that
    #     `solution % d[j] == r[j]`
    #     `increment % d[j] == 0`
    # for all i <= j. In particular, we can add multiples of `increment`
    # to `solution` without changing the first invariant.

    for d, r in zip(divisors[1:], remainders[1:]):
        while solution % d != r:
            solution += increment
        increment *= d

    return solution % increment


assert brut_find("17,x,13,19", 3400) == 3417
assert brut_find("67,7,59,61", 754000) == 754018
assert brut_find("67,x,7,59,61", 779200) == 779210
assert brut_find("67,7,x,59,61", 1261470) == 1261476
assert brut_find("1789,37,47,1889", 1202161480) == 1202161486

# print(brut_find(raw.strip().split("\n")[1], 100000000000000))
assert (
    chinese_remainder(*zip(*make_factors("1789,37,47,1889".split(",")))) == 1202161486
)
print(chinese_remainder(*zip(*make_factors(raw.strip().split("\n")[1].split(",")))))
