from dataclasses import dataclass
from collections import namedtuple
from typing import List
from tqdm import tqdm
from itertools import chain

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

RangeMap = namedtuple("RangeMap", ["destination_start", "source_start", "length"])
Range = namedtuple("Range", ["start", "end"])


@dataclass
class Map:
    source: str
    destination: str
    rangemaps: List[RangeMap]

    @classmethod
    def from_raw(cls, raw: str):
        lines = raw.splitlines()
        assert lines[0].endswith(" map:")
        source, destination = lines[0][:-5].split("-")[::2]
        rangemaps = []
        for line in lines[1:]:
            rangemaps.append(RangeMap(*[int(item) for item in line.split(" ")]))

        return cls(source, destination, rangemaps)

    def get_destination(self, source: int) -> int:
        for rangemap in self.rangemaps:
            offset = source - rangemap.source_start
            if 0 <= offset <= rangemap.length:
                return rangemap.destination_start + offset
        return source

    def get_destination_from_range(self, source_range: Range) -> List[Range]:
        leftover = [Range(source_range.start, source_range.end)]
        # range outside of rangemaps
        output = []
        for rangemap in self.rangemaps:
            _leftover = []
            for lo, hi in leftover:
                rs = rangemap.source_start
                re = rangemap.source_start + rangemap.length

                # print(f"({lo}, {hi}) vs ({rs}, {re})")
                # print("output: ", output)
                # two segments [lo hi) and [rs re)

                # find intersections
                # outside of the range
                if hi < rs or lo > re:
                    print("case1")
                    # [lo hi )          [lo hi)
                    #           [rs re)
                    _leftover.append(Range(lo, hi))
                elif lo < rs and hi <= re:
                    print("case2")
                    # [lo   hi)
                    #    [rs   re)
                    output.append(Range(rangemap.destination_start, rangemap.destination_start + hi - rs))
                    _leftover.append(Range(lo, rs))
                elif lo >= rs and hi <= re:
                    print("case3")
                    #    [lo hi)
                    # [rs         re)
                    output.append(Range(rangemap.destination_start + lo - rs, rangemap.destination_start + hi - rs))
                elif lo >= rs and hi > re:
                    print("case4")

                    #     [lo   hi)
                    # [rs   re)
                    output.append(Range(rangemap.destination_start + lo - rs, re))
                    _leftover.append(Range(re, hi))
                elif lo < rs and hi > re:
                    print("case5")
                    # [lo           hi)
                    #     [rs   re)
                    output.append(Range(rangemap.destination_start, rangemap.destination_start + re - rs))
                    _leftover.append(Range(lo, rs))
                    _leftover.append(Range(re, hi))
                else:
                    raise ValueError(f"Do not hande that case ({lo} {hi}) ({rs} {re}) ({self})")
            leftover = _leftover

            if any([item.start == 0 for item in output]):
                print(source_range, self.source, self.destination, rangemap)
                return None

        output += leftover

        return output


@dataclass
class Almanac:
    seeds: List[int]
    maps: List[Map]

    @property
    def ranges(self):
        return [Range(start, start + length - 1) for start, length in zip(self.seeds[::2], self.seeds[1::2])]

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

    def get_min_location_from_ranges(self):
        ranges = self.ranges

        for mapp in self.maps:
            ranges = chain.from_iterable([mapp.get_destination_from_range(r) for r in ranges])

        return min([r.start for r in ranges])


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
assert ALMANAC.ranges == [Range(79, 92), Range(55, 67)]

assert ALMANAC.get_min_location_from_ranges() == 46

with open("day05.txt", "r") as f:
    raw = f.read()

almanac = Almanac.from_raw(raw)
print(almanac.get_min_location())
print(almanac.get_min_location_from_ranges())
