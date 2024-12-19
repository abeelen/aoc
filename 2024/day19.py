from functools import lru_cache

RAW_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def parse_input(input: str) -> tuple[tuple[str], list[str]]:
    towels, designs = input.strip().split("\n\n")
    towels = tuple(towels.split(", "))
    designs = designs.split("\n")
    return towels, designs


# Recusive function
@lru_cache(maxsize=None)
def is_possible(
    design: str,
    towels: tuple[str],
) -> bool:
    if design in towels:
        return True
    for i in range(1, len(design)):
        if is_possible(design[:i], towels) and is_possible(design[i:], towels):
            return True
    return False


@lru_cache(maxsize=None)
def how_many_possible(design: str, towels: tuple[str]) -> int:
    output = int(design in towels)
    for i in range(1, len(design)):
        output += (design[:i] in towels) * how_many_possible(design[i:], towels)
    return output


def count_possible_designs(towels: tuple[str], designs: list[str]) -> int:
    return sum(is_possible(design, towels) for design in designs)


def count_all_possible_designs(towels: tuple[str], designs: list[str]) -> int:
    return sum(how_many_possible(design, towels) for design in designs)


assert count_possible_designs(*parse_input(RAW_INPUT)) == 6
assert count_all_possible_designs(*parse_input(RAW_INPUT)) == 16

with open("input/day19.txt") as f:
    raw = f.read()
print(count_possible_designs(*parse_input(raw)))
print(count_all_possible_designs(*parse_input(raw)))
