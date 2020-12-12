
from enum import Enum


class Directions(Enum):     
    N = 90
    S = 270
    E = 00
    W = 180


class Ship:
    direction: Directions = Directions.E
    x: int = 0
    y: int = 0
    w_x: int = 10
    w_y: int = 1

    def move(self, instruction: str):
        direction, step = instruction[0], int(instruction[1:])

        if direction == "N" or (self.direction == Directions.N and direction == "F"):
            self.y += step
        elif direction == "S" or (self.direction == Directions.S and direction == "F"):
            self.y -= step
        elif direction == "E" or (self.direction == Directions.E and direction == "F"):
            self.x += step
        elif direction == "W" or (self.direction == Directions.W and direction == "F"):
            self.x -= step
        elif direction == "R":
            self.direction = Directions((self.direction.value - step) % 360)
        elif direction == "L":
            self.direction = Directions((self.direction.value + step) % 360)
        else:
            raise ValueError('Unknown direction : {}'.format(direction))

    def move2(self, instruction: str):
        direction, value = instruction[0], int(instruction[1:])

        if direction == "N":
            self.w_y += value
        elif direction == "S":
            self.w_y -= value
        elif direction == "E":
            self.w_x += value
        elif direction == "W":
            self.w_x -= value
        elif direction == "R":
            d_x = self.w_x - self.x
            d_y = self.w_y - self.y
            if value == 90:
                d_x, d_y = d_y, -d_x
            elif value == 180:
                d_x, d_y = -d_x, -d_y
            elif value == 270:
                d_x, d_y = -d_y, d_x
            else:
                raise ValueError('Unknown angle')
            self.w_x = self.x + d_x
            self.w_y = self.y + d_y
        elif direction == "L":
            d_x = self.w_x - self.x
            d_y = self.w_y - self.y
            if value == 90:
                d_x, d_y = -d_y, d_x
            elif value == 180:
                d_x, d_y = -d_x, -d_y
            elif value == 270:
                d_x, d_y = d_y, -d_x
            else:
                raise ValueError('Unknown angle')
            self.w_x = self.x + d_x
            self.w_y = self.y + d_y
        elif direction == 'F':
            d_x = self.w_x - self.x
            d_y = self.w_y - self.y
            self.x += value * d_x
            self.y += value * d_y
            self.w_x += value * d_x
            self.w_y += value * d_y
        else:
            raise ValueError('Unknown direction : {}'.format(direction))


    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

def navigate(instructions: str) -> int:
    ship = Ship()
    for instruction in instructions.strip().split('\n'):
        ship.move(instruction)
    return ship.manhattan_distance()

def navigate2(instructions: str) -> int:
    ship = Ship()
    for instruction in instructions.strip().split('\n'):
        ship.move2(instruction)
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