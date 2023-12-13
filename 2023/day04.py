from dataclasses import dataclass
from collections import Counter
from typing import List, Set

RAW = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


@dataclass
class Card:
    id: int
    winning_numbers: Set[int]
    numbers: Set[int]

    @classmethod
    def parse_line(cls, line: str) -> "Card":
        card_id, numbers = line.split(": ")
        card_id = int(card_id[5:])
        numbers = numbers.split(" | ")
        winning = set([int(number) for number in numbers[0].split()])
        numbers = set([int(number) for number in numbers[1].split()])
        return cls(card_id, winning, numbers)

    def matching_numbers(self):
        matching_numbers = self.numbers.intersection(self.winning_numbers)
        return len(matching_numbers)

    def win(self):
        matching_numbers = self.matching_numbers()
        if matching_numbers == 0:
            return 0
        return 2 ** (matching_numbers - 1)


@dataclass
class Pile:
    cards: List[Card]

    @classmethod
    def parse_raw(cls, raw: str) -> "Pile":
        cards = []
        for line in raw.split("\n"):
            cards.append(Card.parse_line(line))
        return cls(cards)

    def points(self):
        return sum([card.win() for card in self.cards])

    def more_scratchcards(self):
        counts = [1 for card in self.cards]
        for idx, card in enumerate(self.cards):
            copies = counts[idx]
            for off in range(card.matching_numbers()):
                counts[idx + 1 + off] += copies
        return sum(counts)


PILE = Pile.parse_raw(RAW)
assert PILE.points() == 13
assert PILE.more_scratchcards() == 30

with open("day04.txt", "r") as f:
    raw = f.read()

pile = Pile.parse_raw(raw)
print(pile.points())
print(pile.more_scratchcards())
