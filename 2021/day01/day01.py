
def count_increases(depths):
    increased = 0
    for index in range(1, len(depths)):
        if (depths[index] - depths[index-1]) > 0:
            increased += 1
    return increased


DEPTHS = [199,
200,
208,
210,
200,
207,
240,
269,
260,
263,]

assert(count_increases(DEPTHS) == 7)

with open('input.txt', 'r') as f:
    depths = f.readlines()
    depths = [int(item) for item in depths]

print(count_increases(depths))

def sliding_sum(depths):
    return [sum(depths[index:index+3]) for index in range(len(depths))]

assert(count_increases(sliding_sum(DEPTHS)) == 5)

print(count_increases(sliding_sum(depths)))