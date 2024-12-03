from dataclasses import dataclass
from typing import NamedTuple, List, Set, Tuple, Dict
from collections import deque

class Pos(NamedTuple):
    x: int
    y: int
    
class Dir(NamedTuple):
    dx: int
    dy: int

DIRECTIONS = [Dir(0, 1), Dir(0, -1), Dir(-1, 0), Dir(1, 0)]

class Path(NamedTuple):
    pos: Pos
    steps: int

@dataclass
class Maze:
    start_pos: Pos
    rocks: List[Pos]
    shape: Tuple[int, int]
    
    def steps(self, max_steps=6):
        
        reachable_pos: Set[Pos] = set()
        
        queue = deque([Path(self.start_pos, 0)])
        
        seen: Set[Path] = set()
        
        while queue:
            path = queue.popleft()

            if path.pos in self.rocks:
                continue

            if path in seen:
                continue
            
            if path.steps == max_steps:
                reachable_pos.add(path.pos)
                continue

            seen.add(path)
            
            for _dir in DIRECTIONS:
                new_pos = Pos(path.pos.x + _dir.dx, path.pos.y + _dir.dy)
                queue.append(Path(new_pos, path.steps + 1))

        return len(reachable_pos)


    def distance_from_start(self, start_pos = None):
                
        distances: Dict[Pos, int] = dict()
        
        if start_pos is None:
            queue = deque([Path(self.start_pos, 0)])
        else:
            queue = deque([Path(start_pos, 0)])

        seen: Set[Path] = set()

        while queue:
            path = queue.popleft()
                                    
            if path.pos in distances.keys():
                continue

            if 0 > path.pos.x or path.pos.x >= self.shape[1] or 0 > path.pos.y or path.pos.y >= self.shape[0]:
                continue           

            if path.pos in self.rocks:
                continue

            if path in seen:
                continue
            
            distances[path.pos] = path.steps

            seen.add(path)
            
            for _dir in DIRECTIONS:
                new_pos = Pos(path.pos.x + _dir.dx, path.pos.y + _dir.dy)
                queue.append(Path(new_pos, path.steps + 1))

        return distances   
    
    def im_edges(self, start_pos=None):
        import numpy as np
        
        x_rocks = [item.x for item in self.rocks]
        y_rocks = [item.y for item in self.rocks]
        
        distances = self.distance_from_start(start_pos=start_pos)
        x = [item.x for item in distances]
        y = [item.y for item in distances]
        z = list(distances.values())
        
        img = np.zeros(self.shape)
        img[y, x] = z
        img[y_rocks, x_rocks] = np.nan
        
        return img
    
    @classmethod
    def parse_raw(cls, raw: str) -> "Maze":
        start_pos = None
        rocks: List[Pos] = []
        for y, line in enumerate(raw.split('\n')):
            for x, c in enumerate(line):
                if c == '#':
                    rocks.append(Pos(x, y))
                elif c == 'S':
                    start_pos = Pos(x, y)
                elif c == '.':
                    pass
                else:
                    raise ValueError(f'Unknown tile {c}')
        if start_pos is None:
            raise ValueError('Could not find starting position')
            
        return cls(start_pos, rocks, (y+1, x+1))
        
RAW="""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

MAZE = Maze.parse_raw(RAW)
assert MAZE.steps() == 16

self = MAZE

with open('day21.txt', 'r') as f:
    raw = f.read().strip()
    
maze = Maze.parse_raw(raw)
# print(maze.steps(64))
# Vizualizing the maze and time to reach the edges, their should be a way to compute how many times we could reach a tile