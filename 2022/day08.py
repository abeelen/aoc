
def is_visible(i: int, j: int, quad_map: list[list[int]]) -> bool:
    n_rows = len(quad_map)
    n_cols = len(quad_map[0])

    tree_height = quad_map[i][j]
    visible_top = all([tree_height > quad_map[_][j] for _ in range(i-1, -1, -1)])
    visible_bottom = all([tree_height > quad_map[_][j] for _ in range(i+1, n_rows)])
    visible_left = all([tree_height > quad_map[i][_] for _ in range(0, j)])
    visible_right = all([tree_height > quad_map[i][_] for _ in range(j+1, n_cols)])

    return visible_top or visible_bottom or visible_left or visible_right

def scenic_score(i: int, j:int, quad_map: list[list[int]]) -> int:
    n_rows = len(quad_map)
    n_cols = len(quad_map[0])

    tree_height = quad_map[i][j]
    score_top = 0
    for _ in range(i-1, -1, -1):
        score_top += 1
        if tree_height <= quad_map[_][j]:
            break

    score_bottom = 0
    for _ in range(i+1, n_rows):
        score_bottom += 1
        if tree_height <= quad_map[_][j]:
            break

    score_left = 0
    for _ in range(j-1, -1, -1):
        score_left += 1
        if tree_height <= quad_map[i][_]:
            break

    score_right = 0
    for _ in range(j+1, n_cols):
        score_right += 1
        if tree_height <= quad_map[i][_]:
            break

    return score_top * score_bottom * score_right * score_left


def visible_trees(raw:str) -> int:
    quad_map = [[int(item) for item in row] for row in raw.splitlines()]
    n_rows = len(quad_map)
    n_cols = len(quad_map[0])
    visible_map = []
    for i in range(0, n_rows):
        if i == 0 or i == n_rows:
            visible_map.append([True] * n_cols)
            continue
        visible_row = [True]
        for j in range(1, n_cols-1):
            visible_row.append(is_visible(i, j, quad_map))
        visible_row.append(True)
        visible_map.append(visible_row)

    return sum([sum(item) for item in visible_map])

def max_scenic_score(raw: str) -> int:
    quad_map = [[int(item) for item in row] for row in raw.splitlines()]
    n_rows = len(quad_map)
    n_cols = len(quad_map[0])
    row_max_scenic_scores = []
    for i in range(0, n_rows):
        score_row = []
        for j in range(0, n_cols):
            score_row.append(scenic_score(i, j, quad_map))
        row_max_scenic_scores.append(max(score_row))
    return max(row_max_scenic_scores)

RAW="""30373
25512
65332
33549
35390"""


assert visible_trees(RAW) == 21

with open('day08.txt') as f:
    raw = f.read()

print(visible_trees(raw))

QUAD_MAP = [[int(item) for item in row] for row in RAW.splitlines()]

assert scenic_score(1, 2, QUAD_MAP) == 4
assert scenic_score(3, 2, QUAD_MAP) == 8
assert max_scenic_score(RAW) == 8

print(max_scenic_score(raw))