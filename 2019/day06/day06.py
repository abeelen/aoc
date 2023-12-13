from collections import defaultdict
from typing import List, Dict

INPUT = ["COM)B", 
"B)C",
"C)D",
"D)E",
"E)F",
"B)G",
"G)H",
"D)I",
"E)J",
"J)K",
"K)L",
]

def construct_tree(orbits: List[str]) -> Dict:
    nodes = defaultdict(lambda: set())
    for orbit in orbits:
        planet1, planet2 = orbit.strip().split(')')
        nodes[planet1].add(planet2)
        nodes[planet2].add(planet1)
    return nodes

def bfs(nodes, start):
    queue = [(start, 0)]
    seen = set()
    for node, depth in queue:
        seen.add(node)
        next_nodes = nodes.get(node, [])
        queue += [(new_node, depth + 1) for new_node in next_nodes if new_node not in seen]
        yield node, depth

nodes = construct_tree(INPUT)
assert sum(depth for node, depth in bfs(nodes, 'COM')) == 42

with open('input') as f:
    lines = f.readlines()

nodes = construct_tree(lines)
print(sum(depth for node, depth in bfs(nodes, 'COM')))

# Part 2

INPUT=[
"COM)B",
"B)C",
"C)D",
"D)E",
"E)F",
"B)G",
"G)H",
"D)I",
"E)J",
"J)K",
"K)L",
"K)YOU",
"I)SAN",]
nodes = construct_tree(INPUT)
assert dict(bfs(nodes, 'YOU'))['SAN']-2 == 4

nodes = construct_tree(lines)
print(dict(bfs(nodes, 'YOU'))['SAN']-2)