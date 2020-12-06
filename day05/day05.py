from typing import List, Tuple

SEAT = """FBFBBFFRLR"""


def BSP(low: int = 0, high: int = 127, board: List[str] = "") -> int:
    letter = board.pop(0)
    if letter in ["F", "L"]:
        low = low
        high = low + (high - low - 1) // 2
    if letter in ["B", "R"]:
        low = low + (high - low + 1) // 2
        high = high
    if low == high:
        return low
    else:
        return BSP(low, high, board)


def decode_seat(board: List[str]) -> Tuple[int, int]:
    return BSP(0, 127, board[0:7]), BSP(0, 7, board[7:])


def seat_id(board: str) -> int:
    row, column = decode_seat(list(board))
    return row * 8 + column


assert BSP(0, 127, list(SEAT[0:7])) == 44
assert BSP(0, 7, list(SEAT[7:])) == 5

assert seat_id(SEAT) == 357
assert seat_id("BFFFBBFRRR") == 567
assert seat_id("FFFBBBFRRR") == 119
assert seat_id("BBFFBBFRLL") == 820

with open("day05.txt") as f:
    boarding_passes = [line.strip() for line in f if line]

seat_ids = [seat_id(boarding_pass) for boarding_pass in boarding_passes]
print(max(seat_ids))

seat_ids.sort()


for i in range(1, len(seat_ids)):
    if seat_ids[i] - seat_ids[i - 1] != 1:
        print("Your seat", seat_ids[i - 1] + 1)
