from typing import List

LIST = [1721, 979, 366, 299, 675, 1456]
SUM = 2020

def two_entries(inputs: List[int], total: int) -> List[int]:
    entries = [item for item in inputs if total-item in inputs]
    return entries

def product2(inputs: List[int]) -> int:
    needs = {2020-i: i for i in inputs}

    for i in inputs:
        if i in needs:
            j = needs[i]
            return i * j

def product2b(inputs: List[int], total: int) -> int:
    needs = {total-i: i for i in inputs}

    for i in inputs:
        if i in needs:
            j = needs[i]
            return [i, j]

entries = two_entries(LIST, SUM)
assert 1721 in entries
assert 299 in entries
assert entries[0] * entries[1] == 514579
assert product2(LIST) == 514579

def three_entries(inputs: List[int], total: int) -> List[List[int]]:
    entries = [[item, *two_entries(inputs, total-item)]
               for item in LIST if two_entries(inputs, total-item) != []]
    return entries[0]

def three_entriesb(inputs: List[int], total: int) -> List[List[int]]:
    entries = [[item, *two_entries(inputs, total-item)]
               for item in LIST if product2b(inputs, total-item) != []]
    return entries[0]

def product3(inputs: List[int]) -> int:
    needs = {2020-i-j: (i, j) for i in inputs for j in inputs if i != j}

    for i in inputs:
        if i in needs:
            j, k = needs[i]
            return i * j * k

from itertools import product
def product3b(inputs: List[int]) -> int:
    needs = {2020-i-j: (i, j) for i, j in product(inputs, inputs) if i != j}

    for i in inputs:
        if i in needs:
            j, k = needs[i]
            return i * j * k

entries = three_entries(LIST, SUM)
assert 979 in entries
assert 366 in entries
assert 675 in entries
assert entries[0] * entries[1] * entries[2] == 241861950
assert product3(LIST) == 241861950
assert product3b(LIST) == 241861950

with open('input01.txt') as f:
    inputs = [int(line.strip()) for line in f]

total = 2020
result = two_entries(inputs, total)
print(result, result[0] * result[1])

result = three_entries(inputs, total)
print(result, result[0] * result[1] * result[2])
