from functools import cmp_to_key
from itertools import zip_longest
from typing import Union, Iterable, List, Tuple
import json

Packet = Union[int, List[int], Iterable['Packet']]

Pair = Tuple[Packet, Packet]

DistressSignal = List[Pair]

def parse_packet(raw: str) -> Packet:
    return json.loads(raw)

def parse_pair(raw: str) -> Pair:
    raw1, raw2 = raw.splitlines()
    return parse_packet(raw1), parse_packet(raw2)

def parse_signal(raw: str) -> DistressSignal:
    return [parse_pair(pair) for pair in raw.split('\n\n')]
    
def compare_packet(left: Packet, right: Packet) -> int:
    match (left, right):
        case (int(), int()):
            if left < right:
                return 1
            elif left > right:
                return -1
            else:
                return 0
        case (int(), list()):
            return compare_packet([left], right)
        case (list(), int()):
            return compare_packet(left, [right])
        case (list(), list()):
            for _left, _right in zip_longest(left, right):
                if _left is None:
                    return 1
                elif _right is None:
                    return -1
                else:
                    result = compare_packet(_left, _right)
                    if result != 0:
                        return result
            return 0

def right_order(raw: str) -> int:
    signal = parse_signal(raw)
    good_pairs = [compare_packet(*pair) for pair in signal]
    return sum([i for i, c in enumerate(good_pairs, 1) if c == 1])

def find_divider(raw: str) -> int:
    signal = parse_signal(raw)
    flat_signal = [pair for pairs in signal for pair in pairs]
    divider = [[[2]], [[6]]]
    flat_signal += divider
    sorted_signal = sorted(flat_signal, key=cmp_to_key(compare_packet), reverse=True)
    result = 1
    for i, packet in enumerate(sorted_signal, 1):
        if packet in divider:
            result *= i
    return result



RAW="""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

assert compare_packet([1,1,3,1,1], [1,1,5,1,1]) == 1
assert compare_packet([[1],[2,3,4]], [[1],4]) == 1
assert compare_packet([9], [[8,7,6]]) == -1
assert compare_packet([[4,4],4,4], [[4,4],4,4,4]) == 1
assert compare_packet([7,7,7,7], [7,7,7]) == -1
assert compare_packet([], [3]) == 1
assert compare_packet([[[]]], [[]]) == -1
assert compare_packet([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]) == -1

assert right_order(RAW) == 13

with open('day13.txt') as f:
    raw = f.read()

print(right_order(raw))

assert find_divider(RAW) == 140

print(find_divider(raw))