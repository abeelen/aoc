from dataclasses import dataclass
from collections import namedtuple
from typing import List


RAW = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

RAW_MAP = """seed-to-soil map:
50 98 2
52 50 48"""

Range = namedtuple("Range", ["destination_start", "source_start", "length"])


@dataclass
class Map:
    source: str
    destination: str
    ranges: List[Range]

    @classmethod
    def from_raw(cls, raw: str):
        lines = raw.splitlines()
        assert lines[0].endswith(" map:")
        source, destination = lines[0][:-5].split("-")[::2]
        ranges = []
        for line in lines[1:]:
            ranges.append(Range(*[int(item) for item in line.split(" ")]))

        return cls(source, destination, ranges)

    def get_destination(self, source: int) -> int:
        for range in self.ranges:
            offset = source - range.source_start
            if 0 <= offset <= range.length:
                return range.destination_start + offset
        return source


@dataclass
class Almanac:
    seeds: List[int]
    maps: List[Map]

    @classmethod
    def from_raw(cls, raw: str):
        groups = raw.split("\n\n")
        assert groups[0].startswith("seeds: ")
        seeds = [int(item) for item in groups[0][7:].split()]
        maps = [Map.from_raw(item) for item in groups[1:]]

        assert maps[0].source == "seed"
        destination = maps[0].destination
        for _map in maps[1:]:
            assert _map.source == destination
            destination = _map.destination
        assert maps[-1].destination == "location"
        return cls(seeds, maps)

    def get_location(self, number: int) -> int:
        for _map in self.maps:
            number = _map.get_destination(number)

        return number

    def get_min_location(self):
        locations = [self.get_location(seed) for seed in self.seeds]
        return min(locations)

    def get_min_location_from_pairs(self):
        seeds = []
        for seed_start, seed_length in zip(self.seeds[::2], self.seeds[1::2]):
            seeds += list(range(seed_start, seed_start + seed_length))
        locations = [self.get_location(seed) for seed in seeds]
        return min(locations)


MAP = Map.from_raw(RAW_MAP)

assert MAP.get_destination(79) == 81
assert MAP.get_destination(14) == 14
assert MAP.get_destination(55) == 57
assert MAP.get_destination(13) == 13

ALMANAC = Almanac.from_raw(RAW)

assert ALMANAC.get_location(79) == 82
assert ALMANAC.get_location(14) == 43
assert ALMANAC.get_location(55) == 86
assert ALMANAC.get_location(13) == 35

assert ALMANAC.get_min_location() == 35

assert ALMANAC.get_min_location_from_pairs() == 46

with open("day05.txt", "r") as f:
    raw = f.read()

almanac = Almanac.from_raw(raw)
print(almanac.get_min_location())
print(almanac.get_min_location_from_pairs())
