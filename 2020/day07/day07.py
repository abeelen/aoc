from typing import NamedTuple, Dict, List
from collections import defaultdict
import re

RAW="""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

class Bag(NamedTuple):
    color: str
    contains: Dict[str, int]

def parse_line(line: str)-> Bag:
    color, rest = re.match(r'(.*) bags contain (.*).$', line.strip()).groups()
    contains = {}
    for item in rest.split(', '):
        regex = re.match(r'(\d*) (.*) bag?', item)
        if regex:
            quantity, _color = regex.groups()
            contains[_color] = int(quantity)
    return Bag(color, contains)

def make_bags(raw: str)-> List[Bag]:
    return [parse_line(line) for line in raw.strip().split('\n')]

def parent_map(bags: List[Bag])->Dict[str, List[str]]:
    parents = defaultdict(list)
    for bag in bags:
        for content in bag.contains:
            parents[content].append(bag.color)
    return parents

def can_contains(bags: List[Bag], color: str)-> List[str]:
    parents = parent_map(bags)

    to_look = [color]
    can_contain = set()

    while to_look:
        color = to_look.pop()
        for parent in parents.get(color, []):
            if parent not in can_contain:
                can_contain.add(parent)
                to_look.append(parent)

    return can_contain

with open('day07.txt') as f:
    raw = f.read()

bags = make_bags(raw)
print(len(can_contains(bags, 'shiny gold')))

RAW="""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

def count_bags(dbags: Dict[str, Bag], color: str)->int:
    count = 1
    bag = dbags[color]
    for color, number in bag.contains.items():
        count += number * count_bags(dbags, color)
    return count

dbags = {bag.color: bag for bag in bags}
print(count_bags(dbags, 'shiny gold')-1)
