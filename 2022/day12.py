from dataclasses import dataclass, field
from collections import deque
from itertools import product

from typing import Tuple, Dict, List

@dataclass
class Maze:
    maze: List[List[str]] = field(repr=False)
    graph: Dict[Tuple[int, int], list] = field(repr=False)
    start: Tuple[int, int]
    goal: Tuple[int, int]

    @classmethod
    def parse_raw(cls, raw: str)-> 'Maze':

        maze = raw.splitlines()
        maze = [[item for item in line] for line in maze]
        height = len(maze)
        width = len(maze[0]) if height else 0
        graph = {(i, j): [] for j in range(width) for i in range(height)}
        for row, col in graph.keys():
            if maze[row][col] == 'S':
                start = (row, col)
                maze[row][col] = 'a'
            elif maze[row][col] == 'E':
                goal = (row, col)
                maze[row][col] = 'z'

        for row, col in graph.keys():            
            if row < height - 1 and  ord(maze[row + 1][col]) - ord(maze[row][col]) < 2:
                graph[(row, col)].append(("v", (row + 1, col)))

            if row > 0 and ord(maze[row - 1][col]) - ord(maze[row][col]) < 2:
                graph[(row, col)].append(("^", (row - 1, col)))

            if col < width - 1 and ord(maze[row][col + 1]) - ord(maze[row][col]) < 2:
                graph[(row, col)].append((">", (row, col + 1)))

            if col > 0 and ord(maze[row][col - 1]) - ord(maze[row][col]) < 2:
                graph[(row, col)].append(("<", (row, col - 1)))

        return cls(maze, graph, start, goal)

    def vizualize(self, visited):
        width = max([col for row, col in self.graph.keys()]) + 1
        height = max([row for row, col in self.graph.keys()]) + 1
        lines = [[' '] * width for _ in range(height)]
        row, col = self.start
        lines[row][col] = 'S'
        row, col = self.goal
        lines[row][col] = 'E'

        for row, col in visited:
            lines[row][col] = '.'
        print('\n')
        print('\n'.join(''.join(line) for line in lines))


    def bfs(self):
        queue = deque([("", self.start)])
        visited = set()
        while queue:
            path, current = queue.popleft()
            if current == self.goal:
                return path
            if current in visited:
                continue
            visited.add(current)
            for direction, neighbour in self.graph[current]:
                queue.append((path + direction, neighbour))
            # self.vizualize(visited)
        return -1

    def find_best_trail(self):
        height = len(self.maze)
        width = len(self.maze[0]) if height else 0
        starts = [(row, col) for row, col in product(range(height), range(width)) if self.maze[row][col] == 'a']        
        lengths = []
        for start in starts:
            self.start = start
            lengths.append(self.bfs())
        return min([len(item) for item in lengths if item is not None])

RAW="""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

MAZE = Maze.parse_raw(RAW)
assert len(MAZE.bfs()) == 31

with open('day12.txt') as f:
    raw = f.read().strip()

maze = Maze.parse_raw(raw)
print(len(maze.bfs()))

