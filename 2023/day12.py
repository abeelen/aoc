import re
from typing import List, Tuple
from dataclasses import dataclass
from itertools import product
from tqdm import tqdm
from functools import lru_cache

RAW = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def record_to_groups(records: str) -> List[int]:
    return [item.end() - item.start() for item in re.finditer("#+", records)]


@lru_cache
def solve_recursive(records: str, groups: Tuple[int]) -> int:
    """will cut the records until find 1 char"""
    if len(records) == 0:
        # We are done
        return 1 if len(groups) == 0 else 0
    if records.startswith("."):
        # this we do not care, skip
        return solve_recursive(records[1:], groups)
    if records.startswith("?"):
        # Two possibilities
        return solve_recursive(records.replace("?", ".", 1), groups) + solve_recursive(
            records.replace("?", "#", 1), groups
        )
    if records.startswith("#"):
        if len(groups) == 0:
            # This can not be, as the first record is unknown
            return 0
        if len(records) < groups[0]:
            # We need at least the groups[0] length !!
            return 0
        if any(record == "." for record in records[0 : groups[0]]):
            # This can not be, some records are known within the group
            return 0
        if len(groups) == 1:
            # Only one group left
            return solve_recursive(records[groups[0] :], groups[1:])
        elif len(records) < groups[0] + 1 or records[groups[0]] == "#":
            # not enough records left or
            # This can not be
            return 0
        else:
            # Move to the next group
            return solve_recursive(records[groups[0] + 1 :], groups[1:])


@dataclass
class Row:
    records: str
    groups: List[int]

    def brute_solve(self):
        unknown_state = self.records.count("?")
        template = self.records.replace("?", "{}")
        return sum(
            [record_to_groups(template.format(*items)) == self.groups for items in product("#.", repeat=unknown_state)]
        )

    def solve(self):
        return solve_recursive(self.records, tuple(self.groups))

    def solve_part2(self):
        return solve_recursive(
            "?".join(
                [
                    self.records,
                ]
                * 5
            ),
            tuple(self.groups * 5),
        )

    @classmethod
    def parse_raw(cls, raw: str) -> "Row":
        records, groups = raw.split(" ")
        groups = list(map(int, groups.split(",")))
        return cls(records, groups)


assert record_to_groups("#.#.###") == [1, 1, 3]
assert Row.parse_raw("???.### 1,1,3").brute_solve() == 1
assert Row.parse_raw(".??..??...?##. 1,1,3").brute_solve() == 4
ROWS = [Row.parse_raw(item) for item in RAW.split("\n")]
assert [row.brute_solve() for row in ROWS] == [1, 4, 1, 1, 4, 10]
assert sum([row.brute_solve() for row in ROWS]) == 21
assert sum([row.solve() for row in ROWS]) == 21
assert sum([row.solve_part2() for row in ROWS]) == 525152

with open("day12.txt", "r") as f:
    raw = f.read().strip()

rows = [Row.parse_raw(item) for item in raw.split("\n")]
# print(sum([row.brute_solve() for row in tqdm(rows)]))
print(sum([row.solve() for row in tqdm(rows)]))
print(sum([row.solve_part2() for row in tqdm(rows)]))
