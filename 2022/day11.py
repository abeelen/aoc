from dataclasses import dataclass, field
from typing import Callable
import re
from math import prod
import operator

Operation = Callable[[int], int]
Test = Callable[[int], int]

@dataclass
class Monkey:
    id: int
    operation: Operation = field(repr=False)
    test: Test = field(repr=False)
    items: list[int] = field(default_factory=list)
    nitems: int = 0
    monkey_list: list['Monkey'] = field(default_factory=list, repr=False, init=False)

    @classmethod
    def from_tuple(cls, *args):
        _id, items, operation, test, test_true, test_false = args

        items = [int(item.strip()) for item in items.split(',')]
        operation = Monkey.parse_operation(operation)
        test = Monkey.parse_test(test, test_true, test_false)

        return cls(_id, operation, test, items)

    @staticmethod
    def parse_test(test:int, test_true:int, test_false:int) -> Test:
        fn = lambda x: int(test_true) if x % int(test) == 0 else int(test_false)

        # Keep memory of the modulus value
        fn.modulus = int(test)

        return fn

    @staticmethod
    def parse_operation(s: str)-> Operation:
        left, op, right = s.split()

        match op:
            case '*':
                fn = operator.mul
            case '+':
                fn = operator.add
            case '-':
                fn = operator.sub
            case '/':
                fn = operator.truediv
            case _:
                raise ValueError(f'Unknown operation {s}')

        match [left, right]:
            case ['old', 'old']:
                return lambda x: fn(x, x) 
            case ['old', n]:
                return lambda x: fn(x, int(n)) 
            case [n, 'old']:
                return lambda x: fn(x, int(n)) 
            case [n, m]:
                return lambda x: fn(int(n), int(m))
            case _:
                raise ValueError(f'Unknown operation {s}')

@dataclass(repr=False)
class MonkeyList:
    monkeys: list[Monkey] = field(default_factory=list)
    modulus: int = 1

    def __repr__(self):
        inner_lines = '\n'.join([str(item) for item in self.monkeys])
        return """\
%s
""" % inner_lines

    @classmethod
    def from_raw(cls, raw: str) -> 'MonkeyList':
        PATTERN = 'Monkey (\d):\n  Starting items: (.*)\n  Operation: new = (.*)\n  Test: divisible by (\d*)\n    If true: throw to monkey (\d*)\n    If false: throw to monkey (\d*)\n'

        monkey_list = [Monkey.from_tuple(*args) for args in  re.findall(PATTERN, raw)]
        modulus = 1
        for monkey in monkey_list:
            modulus *= monkey.test.modulus
        return cls(monkey_list, modulus)

    def round(self) -> None:
        for monkey in self.monkeys:
            monkey.nitems += len(monkey.items)
            for item in monkey.items:
                item = monkey.operation(item)
                item = item // 3
                self.monkeys[monkey.test(item)].items.append(item)
            monkey.items.clear()

    def round2(self) -> None:
        for monkey in self.monkeys:
            monkey.nitems += len(monkey.items)
            for item in monkey.items:
                item = monkey.operation(item)
                item = item % self.modulus
                self.monkeys[monkey.test(item)].items.append(item)
            monkey.items.clear()

    def business(self, n=20) -> int:
        for _ in range(n):
            self.round()
        
        most_busy = sorted(self.monkeys, key=lambda item: item.nitems, reverse=True)[:2]
        return prod([item.nitems for item in most_busy])

    def business2(self, n=10_000) -> int:
        for _ in range(n):
            self.round2()
        
        most_busy = sorted(self.monkeys, key=lambda item: item.nitems, reverse=True)[:2]
        return prod([item.nitems for item in most_busy])


RAW = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


MONKEYS = MonkeyList.from_raw(RAW)

assert MONKEYS.business() == 10605

with open('day11.txt') as f:
    raw = f.read()

monkeys = MonkeyList.from_raw(raw)
print(monkeys.business())

MONKEYS = MonkeyList.from_raw(RAW)
assert MONKEYS.business2() == 2713310158

monkeys = MonkeyList.from_raw(raw)
print(monkeys.business2())

