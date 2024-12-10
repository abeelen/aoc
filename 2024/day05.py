from functools import cmp_to_key
from typing import Dict, List, Set, Tuple

RAW_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Rules:
    before: Dict[int, Set[int]]
    after: Dict[int, Set[int]]

    @classmethod
    def from_str(cls, raw: str) -> "Rules":
        before = defaultdict(set)
        after = defaultdict(set)
        for line in raw.split("\n"):
            b, a = map(int, line.split("|"))
            before[a].add(b)
            after[b].add(a)

        return cls(before, after)


def parse_input(raw: str) -> Tuple[Rules, List[List[int]]]:
    rules, updates = raw.split("\n\n")
    rules = Rules.from_str(rules)
    updates = [list(map(int, u.split(","))) for u in updates.split("\n")]

    return rules, updates


def is_right_order(update, rules):
    for index in range(len(update)):
        value = update[index]
        before = update[:index]
        after = update[index + 1 :]
        # check the rules:
        if value in rules.before and not set(before) <= rules.before[value]:
            return False
        if value in rules.after and not set(after) <= rules.after[value]:
            return False
    return True


def sum_valid_middle_number(updates, rules):
    # Keep valid updates only
    valid_updates = [update for update in updates if is_right_order(update, rules)]
    middle_numbers = [update[len(update) // 2] for update in valid_updates]
    return sum(middle_numbers)


def compare_update(update1, update2, rules=None):
    if update2 in rules.after[update1]:
        return -1
    if update2 in rules.before[update1]:
        return 1
    return 0


def sum_incorrect_middle_number(updates, rules):
    invalid_updates = [update for update in updates if not is_right_order(update, rules)]
    key = cmp_to_key(lambda x, y: compare_update(x, y, rules))
    sorted_updates = [sorted(update, key=key) for update in invalid_updates]
    middle_numbers = [update[len(update) // 2] for update in sorted_updates]
    return sum(middle_numbers)


RULES, UPDATES = parse_input(RAW_INPUT)
assert [is_right_order(update, RULES) for update in UPDATES] == [
    True,
    True,
    True,
    False,
    False,
    False,
]


assert sum_valid_middle_number(UPDATES, RULES) == 143
assert sorted([75, 97, 47, 61, 53], key=cmp_to_key(lambda x, y: compare_update(x, y, RULES))) == [97, 75, 47, 61, 53]
assert sum_incorrect_middle_number(UPDATES, RULES) == 123

with open("day05.txt") as f:
    raw = f.read().strip()
rules, updates = parse_input(raw)
print(sum_valid_middle_number(updates, rules))  # 4662
print(sum_incorrect_middle_number(updates, rules))  # 5900
