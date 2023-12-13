from typing import Dict, Tuple, List
import re
from functools import cache
from itertools import product

def parse_raw(raw: str)-> Tuple[Dict[str, List[str]], Dict[str, int]]:
    flows = {}
    maps = {}
    pattern = 'Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)'
    for name, flow, childs in re.findall(pattern, raw):
        flows[name] = int(flow)
        maps[name] = childs.split(', ')

    return maps, flows

@cache
def solve(pos: str, time: int, opened: frozenset, only_me=True) -> int:

    global flows, maps
    if time == 0:
        if not only_me:
            return solve('AA', 26, opened, only_me=True)
        return 0
    
    # What if we go down the path opening nothing at this stage
    score = max([solve(child, time - 1, opened, only_me) for child in maps[pos]])

    # If this position can be opened check agains that too
    if flows[pos] > 0 and pos not in opened:
        # Open the valve for the rest of the game
        new_opened = set(opened)
        new_opened.add(pos)

        # Check against not openning, it takes one minute to open it
        score = max(score, flows[pos] * (time-1) + solve(pos, time - 1, frozenset(new_opened), only_me))
    
    return score

@cache
def solve2(pos: str, pos_elephant: str, time: int, opened: frozenset) -> int:

    global flows, maps
    if time == 0:
        return 0
    
    # What if we go down the path opening nothing at this stage
    score = max([solve2(child, child_elephant, time - 1, opened) for child, child_elephant in product(maps[pos], maps[pos_elephant])])

    # If this position can be opened check agains that too
    if flows[pos] > 0 and pos not in opened and flows[pos_elephant] == 0:
        # Open the valve for the rest of the game
        new_opened = set(opened)
        new_opened.add(pos)

        # Check against not openning, it takes one minute to open it
        score = max(score, flows[pos] * (time-1) + max([solve2(pos, child_elephant, time - 1, frozenset(new_opened)) for child_elephant in maps[pos_elephant]]))
    
    # Test if only the elephan opens
    elif flows[pos] == 0 and  flows[pos_elephant] > 0 and pos_elephant not in opened:
        # Open the valve for the rest of the game
        new_opened = set(opened)
        new_opened.add(pos_elephant)

        # Check against not openning, it takes one minute to open it
        score = max(score, flows[pos_elephant] * (time-1) + max([solve2(child, pos_elephant, time - 1, frozenset(new_opened)) for child in maps[pos]]))

    # We test openning both
    elif flows[pos] > 0 and pos not in opened and flows[pos_elephant] > 0 and pos_elephant not in opened:
        new_opened = set(opened)
        new_opened.add(pos)
        new_opened.add(pos_elephant)

        # Check against not openning, it takes one minute to open it
        score = max(score, (flows[pos] + flows[pos_elephant]) * (time-1) + solve2(pos, pos_elephant, time - 1, frozenset(new_opened)))  

    return score


RAW="""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

maps, flows = parse_raw(RAW)
assert solve('AA', 30, frozenset()) == 1651
assert solve('AA', 26, frozenset(), only_me=False) == 1707


with open('day16.txt') as f:
    raw = f.read()

maps, flows = parse_raw(raw)
solve.cache_clear()
print(solve('AA', 30, frozenset()))
#solve2.cache_clear()
print(solve('AA', 26, frozenset(), only_me=False))