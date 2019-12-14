from typing import List, NamedTuple
from collections import namedtuple
from dataclasses import dataclass

Position = namedtuple("Position", ["x", "y", "z"])
Velocity = namedtuple("Velocity", ["x", "y", "z"])

@dataclass
class Moon():
    pos: Position
    vel: Velocity

    def gravity(self, pos: Position):
        vel = []
        for p1, p2 in zip(self.pos, pos):
            d = p2-p1
            if d>0:
                vel.append(1)
            elif d==0:
                vel.append(0)
            else:
                vel.append(-1)
        return Velocity(*vel)

    def velocity(self):
        pos = []
        for p, v in zip(self.pos, self.vel):
            pos.append(p+v)
        self.pos = Position(*pos)

    @property
    def potential_energy(self):
        return sum([abs(i) for i in self.pos])

    @property
    def kinetic_energy(self):
        return sum([abs(i) for i in self.vel])

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy
    


def gravity(moons: List[Moon]) -> None:
    for moon1 in moons:
        vels = [moon1.vel]
        for moon2 in moons:
            vels.append(moon1.gravity(moon2.pos))
        # Sum all velocities
        moon1.vel = Velocity(*[sum(i) for i in zip(*vels)])

def velocity(moons: List[Moon]) -> None:
    for moon in moons:
        moon.velocity()

def step(moons: List[Moon]) -> None:
    gravity(moons)
    velocity(moons)

moons = [Moon((-1,0,2), (0,0,0)),
        Moon((2,-10,-7), (0,0,0)),
        Moon((4,-8,8), (0,0,0)),
        Moon((3,5,-1), (0,0,0)),]

for _ in range(10):
    step(moons)
assert sum([moon.total_energy for moon in moons]) == 179


moons = [Moon((-8, -10, 0), (0,0,0)),
    Moon((5,5,10), (0,0,0)),
    Moon((2, -7, 3), (0,0,0)),
    Moon((9,-8, -3), (0,0,0)),]

for _ in range(100):
    step(moons)

assert sum([moon.total_energy for moon in moons]) == 1940


"""
<x=-3, y=10, z=-1>
<x=-12, y=-10, z=-5>
<x=-9, y=0, z=10>
<x=7, y=-5, z=-3>
"""
moons = [Moon((-3, 10, -1), (0,0,0)),
    Moon((-12,-10,-5), (0,0,0)),
    Moon((-9, 0, 10), (0,0,0)),
    Moon((7,-5, -3), (0,0,0)),]

for _ in range(1000):
    step(moons)

print(sum([moon.total_energy for moon in moons]))
