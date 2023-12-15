import re
from collections import defaultdict
from dataclasses import dataclass, field


def hash(string: str) -> int:
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256
    return value


assert hash("HASH") == 52

RAW = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

assert sum([hash(item) for item in RAW.split(",")]) == 1320

with open("day15.txt", "r") as f:
    raw = f.read().strip()

print(sum([hash(item) for item in raw.split(",")]))


@dataclass
class HashMap:
    boxes: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))  # works!

    def process(self, raw: str) -> None:
        for instruction in raw.split(","):
            self(instruction)
        return self

    def focusing_power(self) -> int:
        power = 0
        for id, box in self.boxes.items():
            for slot, lens in enumerate(box.values(), start=1):
                power += (id + 1) * slot * int(lens)

        return power

    def __call__(self, instruction: str) -> None:
        match = re.match("(.*)(-|=)(.?)", instruction)

        if not match:
            raise ValueError(f"Could not interpret instructionion {instruction}")

        label, operation, focal = match.groups()
        hsh = hash(label)

        if operation == "=":
            self.boxes[hsh][label] = focal
        elif operation == "-":
            # Remove the lens from the given label
            if label in self.boxes[hsh]:
                del self.boxes[hsh][label]
        else:
            raise ValueError(f"Unknown operation {operation}")


assert HashMap().process(RAW).focusing_power() == 145

print(HashMap().process(raw).focusing_power())
