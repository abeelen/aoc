from dataclasses import dataclass
from typing import List, Dict, Tuple
import re
import math
from itertools import cycle, chain
from collections import defaultdict

RAW = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

RAW_GHOST = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


@dataclass
class WastelandMap:
    instructions: List[str]
    network: Dict[str, Tuple[str, str]]

    def navigate(self):
        node = "AAA"
        for steps, instruction in enumerate(cycle(self.instructions)):
            if node == "ZZZ":
                break
            node = self.network[node][instruction]
        return steps

    def navigate_ghost(self):
        # Find all starting nodes (those ending with 'A')
        nodes = [node for node in self.network.keys() if node.endswith("A")]
        n_nodes = len(nodes)

        # the Z seems to be cyclic, just found the first one for each node
        found_Z = defaultdict(list)

        for steps, instruction in enumerate(cycle(self.instructions)):
            if len(found_Z) == n_nodes:
                break
            for i in range(n_nodes):
                if nodes[i].endswith("Z"):
                    found_Z[i].append(steps)
                nodes[i] = self.network[nodes[i]][instruction]

        steps = list(chain.from_iterable(found_Z.values()))

        return math.lcm(*steps)

    @classmethod
    def parse_raw(cls, raw: str) -> "Map":
        blocks = raw.split("\n\n")
        instructions = [0 if c == "L" else 1 for c in blocks.pop(0)]
        network = {}
        for node, left, right in re.findall("(...) = \((...), (...)\)", blocks[0]):
            network[node] = (left, right)
        return cls(instructions, network)


WASTE = WastelandMap.parse_raw(RAW)
assert WASTE.navigate() == 2

MAP_GHOST = WastelandMap.parse_raw(RAW_GHOST)
assert MAP_GHOST.navigate_ghost() == 6

with open("day08.txt", "r") as f:
    raw = f.read()

waste = WastelandMap.parse_raw(raw)
print(waste.navigate())
print(waste.navigate_ghost())
