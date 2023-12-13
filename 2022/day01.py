from collections import defaultdict
from collections import Counter

def parse_input(lines):
    # elfes = defaultdict(int)
    elfes = Counter()
    i_elfes = 0
    for line in lines.split('\n'):
        if line == '':
            i_elfes += 1
        else:
            elfes[i_elfes] += int(line.strip())
    return elfes

def find_max_calories(elfes):

    #return max(elfes, key=elfes.get)
    # return max(elfes.values())
    return elfes.most_common(1)[0][1]

def find_top3_calories(elfes):
    return sum([item[1] for item in elfes.most_common(3)])
    

    
INPUT = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

assert find_max_calories(parse_input(INPUT)) == 24_000

with open('day01.txt', 'r') as f:
    lines = f.read()

print(find_max_calories(parse_input(lines)))

assert find_top3_calories(parse_input(INPUT)) == 45_000

print(find_top3_calories(parse_input(lines)))
