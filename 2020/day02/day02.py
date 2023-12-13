from __future__ import annotations
from typing import NamedTuple
import re

PASSWORDS = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]


class Password(NamedTuple):
    low: int
    high: int
    char: str
    password: str

    def is_valid(self) -> bool:
        return self.low <= self.password.count(self.char) <= self.high

    def is_valid2(self) -> bool:
        low = self.password[self.low - 1] == self.char
        high = self.password[self.high - 1] == self.char
        return low ^ high

    @staticmethod
    def from_line(line: str) -> Password:
        low, high, char, password = re.match("(\d*)-(\d*) (.): (.*)", line).groups()
        return Password(int(low), int(high), char, password)


assert [Password.from_line(line).is_valid() for line in PASSWORDS] == [True, False, True]
assert [Password.from_line(line).is_valid2() for line in PASSWORDS] == [True, False, False]

with open("day02.txt") as f:
    passwords = [Password.from_line(line.strip()) for line in f]
    print(sum([password.is_valid() for password in passwords]))
    print(sum([password.is_valid2() for password in passwords]))
