from typing import List


def run(start: List[int], turns=10) -> int:
    full_list = []

    for item in start:
        full_list.append(item)
        turns -= 1

    for _ in range(turns):
        item = full_list[-1]
        if item not in full_list[:-1]:
            full_list.append(0)
        else:
            # Last occurence
            last_idx = len(full_list) - full_list[::-1].index(item)
            # previous occurence
            prev_idx = last_idx - 2 - full_list[last_idx - 2 :: -1].index(item)
            full_list.append(last_idx - prev_idx - 1)
    return full_list[-1]


assert run([0, 3, 6], 2020) == 436
assert run([1, 3, 2], 2020) == 1
assert run([3, 1, 2], 2020) == 1836

print(run([10, 16, 6, 0, 1, 17], 2020))
