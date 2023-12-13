from dataclasses import dataclass
from typing import List, Optional
from enum import IntEnum
from collections import Counter


RAW = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


class HandType(IntEnum):
    Five = 6
    Four = 5
    Full = 4
    Three = 3
    Two = 2
    One = 1
    High = 0


CardStrength = dict(zip(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], range(13, 0, -1)))
CardStrength2 = dict(zip(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"], range(13, 0, -1)))


def card_type(cards, part=1):
    count = Counter(cards)

    if part == 2 and "J" in count:
        nJ = count.pop("J")
        most_common = count.most_common()
        if len(most_common) == 0:
            most_common = "A"
        else:
            most_common = most_common[0][0]

        count.update(most_common * nJ)

    count = list(count.values())
    count.sort(reverse=True)
    if count == [5]:
        card_type = HandType.Five
    elif count == [4, 1]:
        card_type = HandType.Four
    elif count == [3, 2]:
        card_type = HandType.Full
    elif count == [3, 1, 1]:
        card_type = HandType.Three
    elif count == [2, 2, 1]:
        card_type = HandType.Two
    elif count == [2, 1, 1, 1]:
        card_type = HandType.One
    elif count == [1, 1, 1, 1, 1]:
        card_type = HandType.High
    else:
        raise ValueError(f"Could not determine type of {cards}")

    return card_type


@dataclass
class Hand:
    cards: str
    bid: Optional[int] = None
    part: Optional[int] = 1

    def __post_init__(self):
        self.type = card_type(self.cards, part=self.part)

        if self.part == 1:
            self.strength = [CardStrength.get(card) for card in self.cards]
        elif self.part == 2:
            self.strength = [CardStrength2.get(card) for card in self.cards]
        else:
            raise ValueError(f"Unknown part {self.part}")

    def __lt__(self, other):
        return self.type < other.type or (self.type == other.type and self.strength < other.strength)


@dataclass
class Game:
    hands: List[Hand]

    @property
    def winnings(self):
        return sum(i * hand.bid for i, hand in enumerate(sorted(self.hands), start=1))

    @classmethod
    def from_raw(cls, raw: str, part=1):
        hands = []
        for line in raw.splitlines():
            cards, bid = line.split(" ")
            bid = int(bid)
            hands.append(Hand(cards, bid, part=part))
        return cls(hands=hands)


assert Hand("AAAAA").type == HandType.Five
assert Hand("AA8AA").type == HandType.Four
assert Hand("23332").type == HandType.Full
assert Hand("TTT98").type == HandType.Three
assert Hand("23432").type == HandType.Two
assert Hand("A23A4").type == HandType.One
assert Hand("23456").type == HandType.High

HANDS = [Hand("33332"), Hand("2AAAA")]
all([hand.type == HandType.Four for hand in HANDS])
assert HANDS[0] > HANDS[1]

HANDS = [Hand("77888"), Hand("77788")]
all([hand.type == HandType.Full for hand in HANDS])
assert HANDS[0] > HANDS[1]

GAME = Game.from_raw(RAW)
assert GAME.winnings == 6440

assert Hand("QJJQ2", part=2).type == HandType.Four
assert Hand("JKKK2", part=2) < Hand("QQQQ2", part=2)
GAME = Game.from_raw(RAW, part=2)
assert GAME.winnings == 5905

with open("day07.txt", "r") as f:
    raw = f.read()

game = Game.from_raw(raw)
print(game.winnings)

game = Game.from_raw(raw, part=2)
print(game.winnings)
