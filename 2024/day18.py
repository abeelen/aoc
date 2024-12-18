from collections import deque, namedtuple

Pos = namedtuple("Pos", ["x", "y"])


def parse_input(raw_input: str) -> list[Pos]:
    return [Pos(*map(int, line.split(","))) for line in raw_input.strip().split("\n")]


def brc(bytes: list[Pos]) -> Pos:
    return Pos(max(b.x for b in bytes), max(b.y for b in bytes))


def bfs(bytes: list[Pos], limit=None, part=1) -> int:
    start = Pos(0, 0)
    end = brc(bytes)

    if limit is not None:
        bytes = bytes[:limit]

    visited = set()
    queue = deque([(start, 0, [])])
    while queue:
        pos, steps, path = queue.popleft()
        if pos == end:
            if part == 1:
                return steps
            elif part == 2:
                return steps, path
        if pos in visited:
            continue

        visited.add(pos)
        path.append(pos)

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            new_pos = Pos(pos.x + dx, pos.y + dy)
            if new_pos in bytes:
                continue
            if new_pos.x < 0 or new_pos.y < 0 or new_pos.x > end.x or new_pos.y > end.y:
                continue
            queue.append((new_pos, steps + 1, path))

    return None


def block_space_brute(bytes: list[Pos], limit=None) -> Pos:
    result = bfs(bytes, limit=limit, part=2)

    while result is not None:
        _, path = result
        # As long as it falls outside of the path, we do not care
        while bytes[limit] not in path:
            limit += 1
        limit += 1
        result = bfs(bytes, limit=limit, part=2)

    return ",".join(map(str, bytes[limit - 1]))


# Brute force is NOT possible....
def block_space_dichotomy(bytes: list[Pos], limit=None) -> str:
    a = limit
    b = len(bytes)

    assert bfs(bytes, limit=a, part=2) is not None

    while a < b:
        m = (a + b) // 2
        result = bfs(bytes, limit=m, part=2)
        if result is not None:
            a = m + 1
        else:
            b = m

    return ",".join(map(str, bytes[a - 1]))


def block_space_bisect(bytes: list[Pos], limit=None) -> str:
    from bisect import bisect_left

    idx = bisect_left(range(len(bytes)), True, lo=limit, key=lambda x: bfs(bytes, limit=x) is None)
    return ",".join(map(str, bytes[idx - 1]))


RAW_INPUT = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

assert bfs(parse_input(RAW_INPUT), limit=12) == 22
assert block_space_brute(parse_input(RAW_INPUT), limit=12) == "6,1"
assert block_space_dichotomy(parse_input(RAW_INPUT), limit=12) == "6,1"
assert block_space_bisect(parse_input(RAW_INPUT), limit=12) == "6,1"

with open("input/day18.txt") as f:
    raw_input = f.read().strip()
bytes = parse_input(raw_input)
print(bfs(bytes, limit=1024))
# print(block_space_brute(parse_input(raw_input), limit=1024))
print(block_space_dichotomy(bytes, limit=1024))
print(block_space_bisect(bytes, limit=1024))  # 33 % faster than the dichotomy
