from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple

class Directions(Enum):     
    N = 90
    S = 270
    E = 00
    W = 180

class Action(NamedTuple):
    action: str
    value: int

    @staticmethod
    def parse(raw: str) -> Action:
        return Action(raw[0], int(raw[1:]))


@dataclass
class Ship:
    direction: Directions = Directions.E
    x: int = 0
    y: int = 0
    w_x: int = 10
    w_y: int = 1

    def move(self, action: Action):
        if action.action == "N":
            self.y += action.value
        elif action.action == "S":
            self.y -= action.value
        elif action.action == "E":
            self.x += action.value
        elif action.action == "W":
            self.x -= action.value
        elif action.action == "R":
            self.direction = Directions((self.direction.value - action.value) % 360)
        elif action.action == "L":
            self.direction = Directions((self.direction.value + action.value) % 360)
        elif action.action == "F":
            if self.direction == Directions.N:
               self.y += action.value
            elif self.direction == Directions.S:
               self.y -= action.value
            elif self.direction == Directions.E:
               self.x += action.value
            elif self.direction == Directions.W:
               self.x -= action.value
            else:
                raise ValueError('Unknown action : {}'.format(action))
        else:
            raise ValueError('Unknown action : {}'.format(action))

    def move2(self, action: Action):

        if action.action == "N":
            self.w_y += action.value
        elif action.action == "S":
            self.w_y -= action.value
        elif action.action == "E":
            self.w_x += action.value
        elif action.action == "W":
            self.w_x -= action.value
        elif action.action == "R":
            assert action.value % 90 == 0, "angle not right"
            for _ in range(action.value //90):
                self.w_x, self.w_y = self.w_y, -self.w_x
        elif action.action == "L":
            assert action.value % 90 == 0, "angle not right"
            for _ in range(action.value //90):
                self.w_x, self.w_y = -self.w_y, self.w_x
        elif action.action == 'F':
            self.x += action.value * self.w_x
            self.y += action.value * self.w_y
        else:
            raise ValueError('Unknown action : {}'.format(action))


    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

def navigate(instructions: str) -> int:
    ship = Ship()
    for action in [Action.parse(line) for line in instructions.strip().split('\n')]:
        ship.move(action)
    return ship.manhattan_distance()

def navigate2(instructions: str) -> int:
    ship = Ship()
    for action in [Action.parse(line) for line in instructions.strip().split('\n')]:
        ship.move2(action)
    return ship.manhattan_distance()

RAW="""F10
N3
F7
R90
F11"""

assert navigate(RAW) == 25
assert navigate2(RAW) == 286

with open('day12.txt') as f:
    raw = f.read()

print(navigate(raw))
print(navigate2(raw))