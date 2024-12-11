# Let's try brute force first...
from functools import lru_cache
from typing import Optional, Tuple


def parse_input(raw_input: str) -> list[str]:
    return raw_input.split()


def blink(rocks: list[int]) -> list[int]:
    new_list = []
    for rock in rocks:
        if rock == "0":
            new_list.append("1")
        elif len(rock) % 2 == 0:  # even number of digits
            len_item = len(rock)
            new_list += [rock[: len_item // 2], str(int(rock[len_item // 2 :]))]
        else:  # If none of the other rules apply
            new_list.append(str(int(rock) * 2024))
    return new_list


def n_blinks(rocks: list[int], n: int) -> list[int]:
    for _ in range(n):
        rocks = blink(rocks)
    return rocks


def n_stones(rocks: list[int], n: int) -> int:
    rocks = n_blinks(rocks, n)
    return len(rocks)


assert " ".join(blink(parse_input("""0 1 10 99 999"""))) == "1 2024 1 0 9 9 2021976"
assert (
    " ".join(n_blinks(parse_input("""125 17"""), 6))
    == "2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2"
)

assert n_stones(parse_input("""125 17"""), 25) == 55312

with open("day11.txt", "r") as f:
    raw_input = f.read().strip()

print(n_stones(parse_input(raw_input), 25))
# This will fail....
# print(n_stones(parse_input(raw_input), 75))

# Let's try to find a pattern
# When we go back to 0, we can know exactly how many stones we will have...
#  print("\n".join([" -> ".join([" ".join(n_blinks([start], i)) for i in range(7)]) for start in map(str, range(0, 10))]))
# 0 -> 1 -> 2024 -> 20 24 -> 2 0 2 4 -> 4048 1 4048 8096 -> 40 48 2024 40 48 80 96
# 1 -> 2024 -> 20 24 -> 2 0 2 4 -> 4048 1 4048 8096 -> 40 48 2024 40 48 80 96 -> 4 0 4 8 20 24 4 0 4 8 8 0 9 6
# 2 -> 4048 -> 40 48 -> 4 0 4 8 -> 8096 1 8096 16192 -> 80 96 2024 80 96 32772608 -> 8 0 9 6 20 24 8 0 9 6 3277 2608
# 3 -> 6072 -> 60 72 -> 6 0 7 2 -> 12144 1 14168 4048 -> 24579456 2024 28676032 40 48 -> 2457 9456 20 24 2867 6032 4 0 4 8
# 4 -> 8096 -> 80 96 -> 8 0 9 6 -> 16192 1 18216 12144 -> 32772608 2024 36869184 24579456 -> 3277 2608 20 24 3686 9184 2457 9456
# 5 -> 10120 -> 20482880 -> 2048 2880 -> 20 48 28 80 -> 2 0 4 8 2 8 8 0 -> 4048 1 8096 16192 4048 16192 16192 1
# 6 -> 12144 -> 24579456 -> 2457 9456 -> 24 57 94 56 -> 2 4 5 7 9 4 5 6 -> 4048 8096 10120 14168 18216 8096 10120 12144
# 7 -> 14168 -> 28676032 -> 2867 6032 -> 28 67 60 32 -> 2 8 6 7 6 0 3 2 -> 4048 16192 12144 14168 12144 1 6072 4048
# 8 -> 16192 -> 32772608 -> 3277 2608 -> 32 77 26 8 -> 3 2 7 7 2 6 16192 -> 6072 4048 14168 14168 4048 12144 32772608
# 9 -> 18216 -> 36869184 -> 3686 9184 -> 36 86 91 84 -> 3 6 8 6 9 1 8 4 -> 6072 12144 16192 12144 18216 2024 16192 8096

# What about a recursive approach and cache.....?


@lru_cache(maxsize=None)
def blink_value(rock: str) -> Tuple[str, Optional[str]]:
    if rock == "0":
        return "1", None
    elif len(rock) % 2 == 0:  # even number of digits
        len_item = len(rock)
        return [rock[: len_item // 2], str(int(rock[len_item // 2 :]))]
    else:  # If none of the other rules apply
        return str(int(rock) * 2024), None


@lru_cache(maxsize=None)
def n_stones_value(rock: str, n: int) -> int:
    # blink once
    result = blink_value(rock)

    if n == 1:
        # This is the last iteration we either have 1 or 2 stones
        return 1 if result[1] is None else 2

    # Recursivity call with the new rock(s)
    count = n_stones_value(result[0], n - 1)
    if result[1] is not None:
        count += n_stones_value(result[1], n - 1)

    return count


def n_stones(rocks: list[int], n: int) -> int:
    n_stones = [n_stones_value(rock, n) for rock in rocks]
    return sum(n_stones)


assert n_stones(parse_input("""125 17"""), 25) == 55312
print(n_stones(parse_input(raw_input), 25))
print(n_stones(parse_input(raw_input), 75))
