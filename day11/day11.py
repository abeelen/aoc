from typing import Dict, List
from collections import namedtuple

RAW ="""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


Pos = namedtuple('Pos', ['x','y'])

def parse_layout(raw: str) -> Dict[Pos, int]:
    lines = raw.strip().split('\n')
    ny = len(lines)
    nx = len(lines[0])
    layout = {}
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == 'L':
                layout[Pos(j, i)] = 0
            elif c == '#':
                layout[Pos(j, i)] = 1

    return layout, nx, ny

def draw_layout(layout: Dict[Pos, int], nx, ny) -> List[str]:
    screen = []
    for i in range(ny):
        line = ""
        for j in range(nx):
            pos = Pos(j,i)
            if pos in layout:
                line += '#' if layout[pos] else 'L'
            else:
                line += '.'
        screen.append(line)
    return screen

def iterate_layout(layout: Dict[Pos, str]):
    next_layout = layout.copy()
    for pos, state in next_layout.items():
        adjacent_seats = sum([
            layout.get(Pos(pos.x-1, pos.y-1), 0) +
            layout.get(Pos(pos.x-1, pos.y), 0) +
            layout.get(Pos(pos.x-1, pos.y+1), 0) +
            layout.get(Pos(pos.x, pos.y-1), 0) +
            layout.get(Pos(pos.x, pos.y+1), 0) +
            layout.get(Pos(pos.x+1, pos.y-1), 0) +
            layout.get(Pos(pos.x+1, pos.y), 0) +
            layout.get(Pos(pos.x+1, pos.y+1), 0)
            ])
        if state == 0 and adjacent_seats == 0:
            next_layout[pos] = 1
        elif state == 1 and adjacent_seats >= 4:
            next_layout[pos] = 0
    return next_layout

def iterate_until(layout: Dict[Pos, str]):
    seats = sum(layout.values())
    layout = iterate_layout(layout)
    new_seats = sum(layout.values())
    while seats != new_seats:
           seats = sum(layout.values())
           layout = iterate_layout(layout) 
           new_seats = sum(layout.values())
    return new_seats


LAYOUT, NX, NY = parse_layout(RAW)   
assert iterate_until(LAYOUT) == 37

with open('day11.txt') as f:
    raw = f.read()
# print(iterate_until(parse_layout(raw)[0]))




def count_seats_directions(layout: Dict[Pos, str], pos: Pos, dx: int, dy:int, nx: int, ny:int):
    while (0 <= pos.x <= nx) and (0 <= pos.y <= ny):
        pos = Pos(pos.x+dx, pos.y+dy)
        if pos in layout:
            return layout[pos]
    return 0

def iterate_layout2(layout: Dict[Pos, str], nx, ny):
    next_layout = layout.copy()
    for pos, state in next_layout.items():
        adjacent_seats = sum([
                count_seats_directions(layout, pos, 0, 1, nx, ny),
                count_seats_directions(layout, pos, 0, -1, nx, ny),
                count_seats_directions(layout, pos, 1, -1, nx, ny),
                count_seats_directions(layout, pos, 1, 0, nx, ny),
                count_seats_directions(layout, pos, 1, 1, nx, ny),
                count_seats_directions(layout, pos, -1, -1, nx, ny),
                count_seats_directions(layout, pos, -1, 0, nx, ny),
                count_seats_directions(layout, pos, -1, 1, nx, ny),
            ])

        if state == 0 and adjacent_seats == 0:
            next_layout[pos] = 1
        elif state == 1 and adjacent_seats >= 5:
            next_layout[pos] = 0
    return next_layout


def iterate_until2(layout: Dict[Pos, str], nx: int, ny: int) -> int:
    seats = sum(layout.values())
    layout = iterate_layout(layout)
    new_seats = sum(layout.values())
    while seats != new_seats:
           seats = sum(layout.values())
           layout = iterate_layout2(layout, nx, ny) 
           new_seats = sum(layout.values())
    return new_seats

assert iterate_until2(LAYOUT, NX, NY) == 26

print(iterate_until2(*parse_layout(raw)))
