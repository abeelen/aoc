from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Cave:
    obstacle: Set[Point] = field(repr=False)

    @classmethod
    def parse_rocks(cls, raw:str) -> 'Cave':
        blocks = []
        for structure in raw.splitlines():
            nodes = structure.split(' -> ')
            for start_node, end_node in zip(nodes, nodes[1:]):
                x_start, y_start = [int(i) for i in start_node.split(',')]
                x_end, y_end = [int(i) for i in end_node.split(',')]
                if x_start == x_end:
                    for _ in range(abs(y_end - y_start) + 1):
                        blocks.append((x_start, min(y_start, y_end)+ _))
                elif y_start == y_end:
                    for _ in range(abs(x_end - x_start) + 1):
                        blocks.append((min(x_start, x_end)+ _, y_start))

        return cls(set(blocks))

    def fill_sand(self):
        # Anything falling below that goes to infinity
        y_min = max([point[1] for point in self.obstacle])
        n_sand = 0
        while True:
            cur = (500, 0)
            while cur[1] < y_min:
                next = (cur[0], cur[1] + 1)
                if next not in self.obstacle:
                    cur = next
                    continue
                next = (cur[0] - 1, cur[1] + 1)
                if next not in self.obstacle:
                    cur = next
                    continue
                next = (cur[0] + 1, cur[1] + 1)
                if next not in self.obstacle:
                    cur = next
                    continue
                # Can not move anymore...
                break
            if cur[1] < y_min:
                self.obstacle.add(cur)
                n_sand += 1
            else:
                break

        return n_sand

    def fill_sand_with_floor(self):
        # Anything falling below that goes to infinity
        y_min = max([point[1] for point in self.obstacle]) + 2
        n_sand = 0
        while True:
            cur = (500, 0)
            while cur[1] < y_min-1:
                next = (cur[0], cur[1] + 1)
                if next not in self.obstacle:
                    cur = next
                    continue
                next = (cur[0] - 1, cur[1] + 1)
                if next not in self.obstacle:
                    cur = next
                    continue
                next = (cur[0] + 1, cur[1] + 1)
                if next not in self.obstacle:
                    cur = next
                    continue
                # Can not move anymore...
                break
            if cur == (500, 0):
                # This one will block everything
                n_sand += 1
                break
            if cur[1] < y_min:
                self.obstacle.add(cur)
                n_sand += 1
        return n_sand

RAW="""498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

assert Cave.parse_rocks(RAW).fill_sand() == 24

with open('day14.txt') as f:
    raw = f.read()

print(Cave.parse_rocks(raw).fill_sand())

assert Cave.parse_rocks(RAW).fill_sand_with_floor() == 93
print(Cave.parse_rocks(raw).fill_sand_with_floor())
