from enum import Enum, IntEnum

# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. 

class HandScore(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

OpponentHand = {'A': 'Rock', 'B': 'Paper', 'C': 'Scissors'}

MyHand = { 'X': 'Rock', 'Y': 'Paper', 'Z': 'Scissors'}

class Score(IntEnum):
    lost = 0
    draw = 3
    win = 6


def score(oppo: str, me:str) -> int:
    if oppo == me:
        score = Score.draw
    elif oppo == 'Rock' and me == 'Paper':
        score = Score.win
    elif oppo == 'Rock' and me == 'Scissors':
        score = Score.lost
    elif oppo == 'Paper' and me == 'Scissors':
        score = Score.win
    elif oppo == 'Paper' and me == 'Rock':
        score = Score.lost
    elif oppo == 'Scissors' and me == 'Paper':
        score = Score.lost
    elif oppo == 'Scissors' and me == 'Rock':
        score = Score.win
    else:
        ValueError('Missing case')
    return score + HandScore[me]

def hand_score(oppo: str, me: str) -> int:
    oppo = OpponentHand.get(oppo, None)
    me = MyHand.get(me, None)

    _score = score(oppo, me)

    return _score 


RAW="""A Y
B X
C Z
"""

def parse_hand(lines):
    stragegy = []
    for line in lines.strip().split('\n'):
        opp, me = line.split(' ')
        stragegy.append(hand_score(opp, me))
    
    return stragegy

assert sum(parse_hand(RAW)) == 15

with open('day02.txt', 'r') as f:
    lines = f.read()

print(sum(parse_hand(lines)))

def hand_strategy(oppo: str, me: str) -> int:
    oppo = OpponentHand.get(oppo, None)
    if me == 'X':
        if oppo == 'Rock':
            me = "Scissors"
        elif oppo == 'Paper':
            me = 'Rock'
        elif oppo == 'Scissors':
            me = 'Paper'
        return score(oppo, me)
    elif me == 'Y':
        # find the proper key...
        return score(oppo, oppo)
    elif me == 'Z':
        if oppo == 'Rock':
            me = 'Paper'
        elif oppo == 'Paper':
            me = 'Scissors'
        elif oppo == 'Scissors':
            me = 'Rock'
        return score(oppo, me)


def parse_strategy(lines):
    stragegy = []
    for line in lines.strip().split('\n'):
        opp, me = line.split(' ')
        stragegy.append(hand_strategy(opp, me))
    return stragegy


assert sum(parse_strategy(RAW)) == 12
print(sum(parse_strategy(lines)))
