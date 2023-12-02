RAW="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

from collections import namedtuple
from typing import List

from dataclasses import dataclass

@dataclass
class Hand:
    red: int
    green: int
    blue: int
    
    @classmethod
    def from_line(cls, raw: str):
        hand = dict([item.split()[::-1] for item in raw.split(', ')])
        return cls(int(hand.get('red', 0)), int(hand.get('green', 0)), int(hand.get('blue', 0)))

    def possible(self, other: "Hand"):
        return self.red <= other.red and self.green <= other.green and self.blue <= other.blue
        
@dataclass
class Game:
    id: int
    hands: List[Hand]

    @classmethod
    def from_line(cls, raw: str):
        header, hands = raw.split(': ')
        return cls(int(header[5:]), [Hand.from_line(item) for item in hands.split('; ')])
        
    def possible(self, other: Hand):
        return all([hand.possible(other) for hand in self.hands])

    def power(self):
        red = max(hand.red for hand in self.hands)
        blue = max(hand.blue for hand in self.hands)
        green = max(hand.green for hand in self.hands)
        return red * blue * green
        

def max_hand_games(games: List[Game], max_hand):
    ids = []
    for game, hands in games.items():
        _max_hand = Hand(0,0,0)
        for hand in hands:
            _max_hand = Hand(max(_max_hand.red, hand.red),
                            max(_max_hand.green, hand.green),
                            max(_max_hand.blue, hand.blue)) 
        if max_hand.red >= _max_hand.red and max_hand.green >= _max_hand.green and max_hand.blue >= _max_hand.blue:
            ids.append(int(game))
    return sum(ids)

GAMES = [Game.from_line(line) for line in RAW.strip().split('\n')]
assert sum([game.id for game in GAMES if game.possible(Hand(12, 13, 14))]) == 8

with open('day02.txt', 'r') as f:
    raw = f.readlines()

games = [Game.from_line(line) for line in raw]
print(sum([game.id for game in games if game.possible(Hand(12, 13, 14))]))

assert sum([item.power() for item in GAMES]) == 2286

print(sum([item.power() for item in games]))