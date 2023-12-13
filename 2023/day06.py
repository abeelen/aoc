from typing import List
from math import prod

RAW = """Time:      7  15   30
Distance:  9  40  200"""


def parse_input(raw: str) -> (List[int], List[int]):
    times, distances = raw.split("\n")
    assert times.startswith("Time: ")
    assert distances.startswith("Distance: ")
    times = [int(t) for t in times.split(":")[1].strip().split()]
    distances = [int(d) for d in distances.split(":")[1].strip().split()]

    return times, distances


def parse_input2(raw: str) -> (int, int):
    times, distances = raw.split("\n")
    assert times.startswith("Time: ")
    assert distances.startswith("Distance: ")
    times = int(times.split(":")[1].strip().replace(" ", ""))
    distances = int(distances.split(":")[1].strip().replace(" ", ""))

    return times, distances


def possible_distances(time):
    return [hold_time * (time - hold_time) for hold_time in range(time)]


def ways_to_beat(time, record_distance):
    records = [item for item in possible_distances(time) if item > record_distance]
    return len(records)


def all_race(times, record_distances):
    records = [ways_to_beat(time, record_distance) for time, record_distance in zip(times, record_distances)]
    return prod(records)


assert all_race(*parse_input(RAW)) == 288
assert ways_to_beat(*parse_input2(RAW)) == 71503

with open("day06.txt", "r") as f:
    raw = f.read().strip()

print(all_race(*parse_input(raw)))
print(ways_to_beat(*parse_input2(raw)))
