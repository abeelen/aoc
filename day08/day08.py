from typing import List

from functools import reduce 
from operator import mul

def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i*n:(i+1)*n], shape[1:]) for i in range(len(lst)//n)]

def image_to_layers(image: str, shape: List[int]) -> List[List[List[int]]]:
    data = [int(i) for i in image]

    n_layers = len(data) // reduce(mul, shape)

    return reshape(data, [n_layers] + shape)

def fewest_zeros(layers: List[List[List[int]]]) -> int:
    n_zeros = [sum([ 1 for line in layer for pix in line if pix ==0]) for layer in layers] 
    min_zeros = min(n_zeros)
    idx = [i for i in range(len(layers)) if n_zeros[i] == min_zeros][0]
    return layers[idx]

def mult_1_2(layer: List[List[int]]) -> int:
    n_ones = sum([ 1 for line in layer for pix in line if pix == 1])
    n_twos = sum([ 1 for line in layer for pix in line if pix == 2])
    return n_ones * n_twos

IMAGE = "123456789012"
SHAPE = [2, 3] # [tall, wide]

assert image_to_layers(IMAGE, SHAPE) == [[[1,2,3],[4,5,6]], [[7,8,9],[0,1,2]]]

with open("input") as f:
    image = f.read().strip()

def stack_layers(layers: List[List[List[int]]], shape: List[int]) -> List[List[int]]:

    n_layers = len(layers)
    output = []
    for j in range(shape[0]):
        line = []
        for i in range(shape[1]):
            k = 0
            while layers[k][j][i] == 2:
                k += 1
            line.append(layers[k][j][i])
        output.append(line)
    return output

IMAGE = "0222112222120000"
SHAPE = [2, 2]
assert image_to_layers(IMAGE, SHAPE) == [[[0, 2], [2, 2]], [[1, 1], [2, 2]], [[2, 2], [1, 2]], [[0, 0], [0, 0]]]
assert stack_layers(image_to_layers(IMAGE, SHAPE), SHAPE) == [[0,1], [1, 0]]

shape = [6, 25]
layers = image_to_layers(image, shape)
layer = fewest_zeros(layers)
print(mult_1_2(layer))

image = stack_layers(layers, shape)

# Replace white by '*' 
print("\n".join(["".join(["+" if (pix == 1) else " " for pix in line]) for line in image]))