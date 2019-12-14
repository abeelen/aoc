from typing import List, NamedTuple, Tuple
from collections import namedtuple
from dataclasses import dataclass

Position = namedtuple("Position", ["x", "y", "z"])
Velocity = namedtuple("Velocity", ["x", "y", "z"])

@dataclass
class Moon():
    pos: Position
    vel: Velocity

    def __init__(self, pos: Tuple):
        self.pos = Position(*pos)
        self.vel = Velocity(0,0,0)

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

    @property
    def checksum(self):
        return self.pos + self.vel
    
    @property
    def checksum_x(self):
        return (self.pos.x, self.vel.x)

    @property
    def checksum_y(self):
        return (self.pos.y, self.vel.y)

    @property
    def checksum_z(self):
        return (self.pos.z, self.vel.z)

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

def total_energy(moons: List[Moon]) -> int:
    return sum([moon.total_energy for moon in moons])

def potential_energy(moons: List[Moon]) -> int:
    return sum([moon.potential_energy for moon in moons])


def kinetic_energy(moons: List[Moon]) -> int:
    return sum([moon.kinetic_energy for moon in moons])


def step(moons: List[Moon]) -> None:
    gravity(moons)
    velocity(moons)

moons = [Moon((-1,0,2)),
        Moon((2,-10,-7)),
        Moon((4,-8,8)),
        Moon((3,5,-1)),]

from copy import deepcopy

def checksum(moons: List[Moon]) -> Tuple:
    return tuple([moon.checksum for moon in moons])

def checksum_x(moons: List[Moon]) -> Tuple:
    return tuple([moon.checksum_x for moon in moons])

def checksum_y(moons: List[Moon]) -> Tuple:
    return tuple([moon.checksum_y for moon in moons])

def checksum_z(moons: List[Moon]) -> Tuple:
    return tuple([moon.checksum_z for moon in moons])


def force_loop(moons: List[Moon], func=checksum) -> int:
    moons = deepcopy(moons)
    universe = []
    i = 0
    while (func(moons) not in universe):
        universe.append(func(moons))
        step(moons)
        i+=1
    return i

# assert force_loop(moons) == 2772

from math import gcd
def xyz_gcd(moons: List[Moon]) -> int:
    loops = [force_loop(moons, check) for check in [checksum_x, checksum_y, checksum_z]]
    n = loops[0]
    for i in loops[1:]:
        n = n*i // gcd(n, i)
    return n

assert xyz_gcd(moons) == 2772

def energy_loop(moons: List[Moon], func_energy=kinetic_energy) -> List[int]:
    moons = deepcopy(moons)
    energies = []
    energy = func_energy(moons)
    i = 0

    while(energy not in energies):
        print(energies, energy)
        energies.append(energy)
        step(moons)
        energy = func_energy(moons)
        i+=1
    print(energies, energy)
    return i


moons = [Moon((-8, -10, 0)),
    Moon((5,5,10)),
    Moon((2, -7, 3)),
    Moon((9,-8, -3)),]

# assert loop(moons) == 4686774924
assert xyz_gcd(moons) == 4686774924


"""
<x=-3, y=10, z=-1>
<x=-12, y=-10, z=-5>
<x=-9, y=0, z=10>
<x=7, y=-5, z=-3>
"""
moons = [Moon((-3, 10, -1)),
    Moon((-12,-10,-5)),
    Moon((-9, 0, 10)),
    Moon((7,-5, -3)),]

print("go")
print(xyz_gcd(moons))