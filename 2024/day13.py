import re
from collections import namedtuple
from typing import List, Optional, Tuple

RAW_INPUT = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

Button = namedtuple("Button", ["dx", "dy"])
Prize = namedtuple("Prize", ["x", "y"])
Machine = namedtuple("Machine", ["A", "B", "Prize"])

MACHINE_PATTERN = re.compile("Button A: X\+(\d*), Y\+(\d*)\nButton B: X\+(\d*), Y\+(\d*)\nPrize: X=(\d*), Y=(\d*)")


def parse_input(raw_input: str, unit_convertion: int = 0) -> List[Machine]:
    machines = []
    for match in MACHINE_PATTERN.finditer(raw_input):
        A = Button(int(match.group(1)), int(match.group(2)))
        B = Button(int(match.group(3)), int(match.group(4)))
        P = Prize(int(match.group(5)) + unit_convertion, int(match.group(6)) + unit_convertion)
        machines.append(Machine(A, B, P))

    return machines


# Classical case of linear algebra...
def invert_M(matrix: List[List[int]]) -> List[List[int]]:
    """[a, b]
        [c, d]

    det = 1 / (ad - bc)

    -> det * [d, -b]
             [-c, a]
    """
    a, b = matrix[0]
    c, d = matrix[1]
    det = a * d - b * c
    if det == 0:
        return None
    return [[d / det, -b / det], [-c / det, a / det]]


def solve_machine(machine: Machine) -> Optional[Tuple[int, int]]:
    """A * a + B * b = P
    [A.x, B.x] * [a] = [P.x]
    [A.y, B.y]   [b]   [P.y]
    A * s = P
    s = A^-1 * P
    """
    M = [[machine.A.dx, machine.B.dx], [machine.A.dy, machine.B.dy]]
    P = [machine.Prize.x, machine.Prize.y]

    inv_M = invert_M(M)
    if inv_M is None:
        return None
    solution = [inv_M[0][0] * P[0] + inv_M[0][1] * P[1], inv_M[1][0] * P[0] + inv_M[1][1] * P[1]]

    # we need integer output
    solution = list(map(round, solution))
    # check that the integer solution is still valid
    result_x = solution[0] * machine.A.dx + solution[1] * machine.B.dx
    result_y = solution[0] * machine.A.dy + solution[1] * machine.B.dy
    if result_x != machine.Prize.x or result_y != machine.Prize.y:
        return None
    return solution


def machine_prize(machine: Machine, token_price: dict) -> int:
    solution = solve_machine(machine)
    if solution is None:
        return 0
    nA, nB = solution
    return token_price["A"] * nA + token_price["B"] * nB


def win_all_possible(machines: List[Machine], token_price: dict) -> int:
    return sum(machine_prize(machine, token_price) for machine in machines)


TOKEN_PRICE = {"A": 3, "B": 1}
machines = R = parse_input(RAW_INPUT)

assert solve_machine(machines[0]) == [80, 40]
assert solve_machine(machines[1]) is None
assert solve_machine(machines[3]) is None
assert solve_machine(machines[2]) == [38, 86]

assert machine_prize(machines[0], TOKEN_PRICE) == 280
assert machine_prize(machines[2], TOKEN_PRICE) == 200
assert win_all_possible(machines, TOKEN_PRICE) == 480

with open("day13.txt", "r") as f:
    input_raw = f.read().strip()

machines = parse_input(input_raw)
print(win_all_possible(machines, TOKEN_PRICE))
machines = parse_input(input_raw, unit_convertion=10000000000000)
print(win_all_possible(machines, TOKEN_PRICE))
