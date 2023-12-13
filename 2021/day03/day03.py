INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

from collections import Counter

def count_bits(input):
    n_bits = len(input[0])
    bits = [Counter() for _ in range(n_bits)]
    for item in input:
        for idx in range(n_bits):
            bits[idx].update(item[idx])
    return bits

def to_gamma(bits):
    return int(''.join([bit.most_common()[0][0] for bit in bits]), 2)

def to_epsilon(bits):
    return int(''.join([bit.most_common()[-1][0] for bit in bits]), 2)

BITS = count_bits(INPUT.split('\n'))
assert to_gamma(BITS) * to_epsilon(BITS) == 198

with open('input.txt', 'r') as f:
    input = f.readlines()

bits = count_bits(input)
print(to_gamma(bits) * to_epsilon(bits))

def oxygen(input):
    result = []
    n_bits = len(input[0])
    sub_input = input.copy()
    for idx in range(n_bits):
        bits = count_bits(sub_input)
        value_one = bits[idx].get('1', 0)
        value_zero = bits[idx].get('0', 0)
        if value_one >= value_zero:
            value = '1'
        else:
            value = '0'
        
        result.append(value)
        sub_input = [item for item in sub_input if item[idx] == value]
        if len(sub_input) == 1:
            return int(sub_input[0], 2)
    return int(''.join(result), 2)

def co2(input):
    result = []
    n_bits = len(input[0])
    sub_input = input.copy()
    for idx in range(n_bits):
        bits = count_bits(sub_input)
        value_one = bits[idx].get('1', 0)
        value_zero = bits[idx].get('0', 0)
        if value_one < value_zero:
            value = '1'
        else:
            value = '0'
        
        result.append(value)
        sub_input = [item for item in sub_input if item[idx] == value]
        if len(sub_input) == 1:
            return int(sub_input[0], 2)
    
    return int(''.join(result), 2)

assert oxygen(INPUT.split('\n')) == 23
assert co2(INPUT.split('\n')) == 10

print(oxygen(input) * co2(input))