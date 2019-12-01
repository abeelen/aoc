def fuel(mass: int) -> int:
    return mass // 3 - 2

assert(fuel(12) == 2)
assert(fuel(14) == 2)
assert(fuel(1969) == 654)
assert(fuel(100756) == 33583)

with open('input') as f:
    masses = [int(mass.strip()) for mass in f]

total_fuel = sum([fuel(mass) for mass in masses])

def fuel_for_fuel(mass: int) -> int:
    total_fuel = 0
    left_fuel = fuel(mass)
    while left_fuel > 0:
        total_fuel += left_fuel
        left_fuel = fuel(left_fuel)

    return total_fuel


assert(fuel_for_fuel(14) == 2)
assert(fuel_for_fuel(1969) == 966)
assert(fuel_for_fuel(100756) == 50346)

total_fuel = sum([fuel_for_fuel(mass) for mass in masses])
