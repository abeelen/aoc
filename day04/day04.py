from __future__ import annotations
from typing import NamedTuple
import re

FOUR_DIGIT = re.compile("\d{4}")
HEIGHT = re.compile("(\d*)(cm|in)$")
HAIR_COLOR = re.compile("^#([0-9a-f]){6}$")
EYE_COLOR = re.compile("^(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)$")
PASSPORT = re.compile("^(\d){9}$")


class Passport(NamedTuple):
    byr: str = None  # Birth Year
    iyr: str = None  # Issue Year
    eyr: str = None  # Expiration Year
    hgt: str = None  # Height
    hcl: str = None  # Hair Color
    ecl: str = None  # Eye Color
    pid: str = None  # Password ID
    cid: str = None  # Country ID

    def is_valid(self):
        return (
            (self.byr is not None)
            and (self.iyr is not None)
            and (self.eyr is not None)
            and (self.hgt is not None)
            and (self.hcl is not None)
            and (self.ecl is not None)
            and (self.pid is not None)
        )

    def is_valid2(self):
        if not self.is_valid(): return False
        height = HEIGHT.match(self.hgt).groups() if  HEIGHT.match(self.hgt) else None
        return (
            FOUR_DIGIT.match(self.byr) is not None
            and (1920 <= int(self.byr) <= 2002)
            and FOUR_DIGIT.match(self.iyr) is not None
            and (2010 <= int(self.iyr) <= 2020)
            and FOUR_DIGIT.match(self.eyr) is not None
            and (2020 <= int(self.eyr) <= 2030)
            and height is not None
            and (150 <= int(height[0]) <= 193 if height[1] == "cm" else 59 <= int(height[0]) <= 76)
            and HAIR_COLOR.match(self.hcl) is not None
            and EYE_COLOR.match(self.ecl) is not None
            and PASSPORT.match(self.pid) is not None
        )

    @staticmethod
    def parse(line: str) -> Passport:
        return Passport(**dict(tuple(item.split(":")) for item in line.split()))


RAW = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

assert [Passport.parse(item).is_valid() for item in RAW.split("\n\n")] == [True, False, True, False]
assert sum([Passport.parse(item).is_valid() for item in RAW.split("\n\n")]) == 2

with open("day04.txt") as f:
    raw = f.read()

print(sum([Passport.parse(item).is_valid() for item in raw.split("\n\n")]))

RAW_INVALID = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

assert sum([Passport.parse(item).is_valid2() for item in RAW_INVALID.split("\n\n")]) == 0

RAW_VALID="""pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

assert sum([Passport.parse(item).is_valid2()  for item in RAW_VALID.split("\n\n")]) == 4

print(sum([Passport.parse(item).is_valid2() for item in raw.split("\n\n")]))
