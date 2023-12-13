from collections import Counter


def item_priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    elif item.isupper():
        return ord(item) - ord('A') + 27
    else:
        raise ValueError('is this a ascii char ??')


def parse_rucksack(compartiment):
    n_items = len(compartiment)
    one = set(compartiment[0:n_items//2])
    two = set(compartiment[n_items//2:])
    common_item = one & two
    assert len(common_item) == 1
    common_item = common_item.pop()
    return item_priority(common_item)

RAW="""vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

assert sum([parse_rucksack(line) for line in RAW.split('\n')]) == 157

with open('day04.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

print(sum([parse_rucksack(line) for line in lines]))

def find_badge_priority(ruck1, ruck2, ruck3):
    common_item =  set(ruck1) & set(ruck2) & set(ruck3)
    assert len(common_item) == 1
    common_item = common_item.pop()
    return item_priority(common_item)


def parse_lines(lines):
    n_lines = len(lines)

    return sum([find_badge_priority(*lines[i: i+3]) for i in range(0, n_lines, 3)])

assert parse_lines(RAW.split('\n')) == 70

print(parse_lines(lines))