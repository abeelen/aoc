from typing import Tuple, Dict, List

from collections import namedtuple
from collections import defaultdict
from math import ceil

Reactant = namedtuple("Reactant", ['quantity', 'specie'])
Reaction = namedtuple("Reaction", ['quantity', 'reactants'])

def parse_item(input_str: str) -> Tuple[int, str]:
    quantity, item = input_str.split(' ')
    return int(quantity), item

def parse_reactions(input_str: str)-> Dict[str, Tuple[int, List[Reactant]]]:

    reactions = {}

    for line in input_str.strip().split('\n'):
        inputs, output = line.split(' => ')
        output_quantity, output = parse_item(output)

        reactants = []
        for reactant in inputs.split(', '):
            reactants.append(Reactant(*parse_item(reactant)))
        
        reactions[output] = (output_quantity, reactants)
    
    return reactions

def backreac(item: str, amount: int, surplus: Dict[str, int]) -> Dict[str, int]:

    unitary_quantity, reactants = REACTIONS[item]

    number_of_reactions = ceil(amount / unitary_quantity)

    surplus[item] += number_of_reactions * unitary_quantity - amount

    items_needed = {}
    for reactant in reactants:
        amount_needed = reactant.quantity * number_of_reactions
        from_surplus = min(amount_needed, surplus[reactant.specie])
        amount_needed -= from_surplus
        surplus[reactant.specie] -= from_surplus
        items_needed[reactant.specie] = amount_needed

    return items_needed


def ore_needed(item: str, amount: int) -> int:

    item_needed = defaultdict(int)
    surplus = defaultdict(int)

    ore = 0
    
    item_needed[item] = amount

    while item_needed:
        item, amount = item_needed.popitem()
        
        items = backreac(item, amount, surplus)

        # pick up ORE if present
        if 'ORE' in items:
            ore += items.pop('ORE')
        
        for item, quantity in items.items():
            item_needed[item] += quantity

    return ore

RAW="""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

REACTIONS = parse_reactions(RAW)
assert ore_needed('FUEL', 1) == 31

RAW = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

REACTIONS = parse_reactions(RAW)
assert ore_needed('FUEL', 1) == 165

RAW = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

REACTIONS = parse_reactions(RAW)
assert ore_needed('FUEL', 1) == 13312

RAW = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""
REACTIONS = parse_reactions(RAW)
assert ore_needed('FUEL', 1) == 180697

RAW = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
REACTIONS = parse_reactions(RAW)
assert ore_needed('FUEL', 1) == 2210736

with open('input') as f:
    raw = f.read()
REACTIONS = parse_reactions(raw)
print(ore_needed('FUEL', 1))

def bisect_search(a: int, b: int, ore_stock: int, max_iter: int = 1000):

    i = 0

    while i < max_iter:
        c = int((a + b) // 2)
        c_ore =  ore_needed('FUEL', c)
        if c_ore == ore_stock or (b-a) // 2 == 0:
            return c
        if c_ore < ore_stock:
            a = c
        else: 
            b = c
        i += 1

    return None

ore_stock = 1000000000000
print(bisect_search(1, 1e6, ore_stock))