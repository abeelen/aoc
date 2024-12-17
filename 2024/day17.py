import re
from dataclasses import dataclass
from enum import Enum
from typing import List


class Opcode(Enum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


@dataclass
class Computer:
    A: int
    B: int
    C: int
    program: List[int]

    @classmethod
    def from_raw(cls, raw_input: str) -> "Computer":
        pattern = "Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.*)"
        A, B, C, program = re.match(pattern, raw_input.strip()).groups()
        program = list(map(int, program.split(",")))
        return cls(int(A), int(B), int(C), program)

    def combo_operand(self, operand: int) -> int:
        if operand < 4:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        elif operand == 7:
            raise ValueError("Reserved operand")

    def run(self):
        output = []

        ptr = 0

        while True:
            if ptr >= len(self.program):
                break
            opcode = self.program[ptr]
            operand = self.program[ptr + 1]

            if Opcode(opcode) == Opcode.adv:
                """The adv instruction (opcode 0) performs division.
                The numerator is the value in the A register.
                The denominator is found by raising 2 to the power of the instruction's combo operand.
                (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
                The result of the division operation is truncated to an integer and then written to the A register."""
                numerator = self.A
                denominator = 2 ** self.combo_operand(operand)
                self.A = int(numerator / denominator)
            elif Opcode(opcode) == Opcode.bxl:
                """The bxl instruction (opcode 1) 
                calculates the bitwise XOR of register B 
                and the instruction's literal operand, 
                then stores the result in register B."""
                self.B = self.B ^ operand
            elif Opcode(opcode) == Opcode.bst:
                """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
                (thereby keeping only its lowest 3 bits),
                then writes that value to the B register."""
                self.B = self.combo_operand(operand) % 8
            elif Opcode(opcode) == Opcode.jnz:
                """The jnz instruction (opcode 3) does nothing if the A register is 0.
                However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand;
                if this instruction jumps, the instruction pointer is not increased by 2 after this instruction."""
                if self.A != 0:
                    ptr = operand
                    continue
            elif Opcode(opcode) == Opcode.bxc:
                """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
                then stores the result in register B.
                (For legacy reasons, this instruction reads an operand but ignores it.)"""
                self.B = self.B ^ self.C
            elif Opcode(opcode) == Opcode.out:
                """The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
                then outputs that value. (If a program outputs multiple values, they are separated by commas.)"""
                output.append(self.combo_operand(operand) % 8)
            elif Opcode(opcode) == Opcode.bdv:
                """The bdv instruction (opcode 6) works exactly like the adv instruction except
                that the result is stored in the B register.
                (The numerator is still read from the A register.)"""
                numerator = self.A
                denominator = 2 ** self.combo_operand(operand)
                self.B = int(numerator / denominator)
            elif Opcode(opcode) == Opcode.cdv:
                """The cdv instruction (opcode 7) works exactly like the adv instruction 
                except that the result is stored in the C register.
                (The numerator is still read from the A register.)"""
                numerator = self.A
                denominator = 2 ** self.combo_operand(operand)
                self.C = int(numerator / denominator)
            else:
                raise ValueError("Invalid opcode")

            ptr += 2

        return ",".join(map(str, output))

    def replicate(self):
        "FAIL...."
        # brute force on A, but stop as soon as possible
        init_A = 0

        def combo_operand(operand: int, A, B, C) -> int:
            if operand < 4:
                return operand
            elif operand == 4:
                return A
            elif operand == 5:
                return B
            elif operand == 6:
                return C
            elif operand == 7:
                raise ValueError("Reserved operand")

        while True:
            A = init_A
            B = self.B
            C = self.C

            ptr = 0
            output = []

            while True:
                if output != self.program[: len(output)]:
                    break

                if ptr >= len(self.program):
                    break
                opcode = self.program[ptr]
                operand = self.program[ptr + 1]

                if Opcode(opcode) == Opcode.adv:
                    """The adv instruction (opcode 0) performs division.
                    The numerator is the value in the A register.
                    The denominator is found by raising 2 to the power of the instruction's combo operand.
                    (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
                    The result of the division operation is truncated to an integer and then written to the A register."""
                    numerator = A
                    denominator = 2 ** combo_operand(operand, A, B, C)
                    A = int(numerator / denominator)
                elif Opcode(opcode) == Opcode.bxl:
                    """The bxl instruction (opcode 1) 
                    calculates the bitwise XOR of register B 
                    and the instruction's literal operand, 
                    then stores the result in register B."""
                    B = B ^ operand
                elif Opcode(opcode) == Opcode.bst:
                    """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
                    (thereby keeping only its lowest 3 bits),
                    then writes that value to the B register."""
                    B = combo_operand(operand, A, B, C) % 8
                elif Opcode(opcode) == Opcode.jnz:
                    """The jnz instruction (opcode 3) does nothing if the A register is 0.
                    However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand;
                    if this instruction jumps, the instruction pointer is not increased by 2 after this instruction."""
                    if A != 0:
                        ptr = operand
                        continue
                elif Opcode(opcode) == Opcode.bxc:
                    """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
                    then stores the result in register B.
                    (For legacy reasons, this instruction reads an operand but ignores it.)"""
                    B = B ^ C
                elif Opcode(opcode) == Opcode.out:
                    """The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
                    then outputs that value. (If a program outputs multiple values, they are separated by commas.)"""
                    output.append(combo_operand(operand, A, B, C) % 8)
                elif Opcode(opcode) == Opcode.bdv:
                    """The bdv instruction (opcode 6) works exactly like the adv instruction except
                    that the result is stored in the B register.
                    (The numerator is still read from the A register.)"""
                    numerator = A
                    denominator = 2 ** combo_operand(operand, A, B, C)
                    B = int(numerator / denominator)
                elif Opcode(opcode) == Opcode.cdv:
                    """The cdv instruction (opcode 7) works exactly like the adv instruction 
                    except that the result is stored in the C register.
                    (The numerator is still read from the A register.)"""
                    numerator = A
                    denominator = 2 ** combo_operand(operand, A, B, C)
                    C = int(numerator / denominator)
                else:
                    raise ValueError("Invalid opcode")

                ptr += 2

            if output == self.program:
                return init_A

            if len(output) <= len(self.program):
                init_A += 1
            else:
                init_A += 1


COMPUTER = Computer(0, 0, 9, [2, 6])
COMPUTER.run()
assert COMPUTER.B == 1

assert Computer(10, 0, 0, [5, 0, 5, 1, 5, 4]).run() == "0,1,2"
COMPUTER = Computer(2024, 0, 0, [0, 1, 5, 4, 3, 0])
assert COMPUTER.run() == "4,2,5,6,7,7,7,7,3,1,0"
assert COMPUTER.A == 0

COMPUTER = Computer(0, 29, 0, [1, 7])
COMPUTER.run()
assert COMPUTER.B == 26

COMPUTER = Computer(0, 2024, 43690, [4, 0])
COMPUTER.run()
assert COMPUTER.B == 44354

RAW_INPUT = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

COMPUTER = Computer.from_raw(RAW_INPUT)
assert COMPUTER.run() == "4,6,3,5,6,3,5,2,1,0"

with open("day17.txt", "r") as f:
    raw_input = f.read().strip()
computer = Computer.from_raw(raw_input)
print(computer.run())

RAW_INPUT = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


# 4HbQ answer for part 2
def recursive_A(raw_input: str) -> int:
    pattern = "Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.*)"
    A, B, C, program_str = re.match(pattern, raw_input.strip()).groups()
    program = list(map(int, program_str.split(",")))
    A, B, C = map(int, [A, B, C])

    # Check last digit, starting with 0
    todo = [(-1, 0)]
    for i, a in todo:
        # Test all possible A values, (instruction 5, 4 in program output the A value % 8)
        for a in range(a, a + 8):
            result = Computer(a, 0, 0, program).run()
            result = result.replace(",", "")
            if result == program_str.replace(",", "")[i:]:
                todo += [(i - 1, a * 8)]
                if result == program_str.replace(",", ""):
                    return a

    # A = 0
    # result = Computer(A, B, C, program).run()
    # A += 1
    # result = Computer(A, B, C, program).run()
    # while len(program_str) != len(result):
    #     result = Computer(A, B, C, program).run()
    #     print(A, result, program_str)
    #     A *= 2

    return A


assert recursive_A(RAW_INPUT) == 117440
print(recursive_A(raw_input))

# COMPUTER = Computer.from_raw(RAW_INPUT)
# assert COMPUTER.replicate() == 117440

# computer = Computer.from_raw(raw_input)
# print(computer.replicate())
