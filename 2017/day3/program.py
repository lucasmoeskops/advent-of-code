from itertools import starmap
from math import ceil, sqrt
from sys import argv

memory_square = int(argv[1]) if len(argv) > 1 else 347991


# Part 1

root = int(ceil(sqrt(memory_square)))
# Make sure it is an odd root
root = root + 1 if root % 2 == 0 else root
field = ((root - 2)**2, root**2)
quadrant = max(1, (field[1] - field[0]) // 4)
answer1 = root // 2 + abs(quadrant // 2 - (memory_square - field[0]) % quadrant)
print('Distance from square {} to 1 is {}'.format(memory_square, answer1))


# Part 2

def xy_to_index(x, y):
    radius = max(abs(x), abs(y))
    root = radius * 2 + 1
    field = ((root - 2)**2, root**2)
    quadrant_size = (field[1] - field[0]) // 4
    if -y == radius and x != radius:
        return field[0] + quadrant_size + radius - x
    elif -x == radius and -y != radius:
        return field[0] + 2 * quadrant_size + radius + y
    elif y == radius and -x != radius:
        return field[0] + 3 * quadrant_size + radius + x
    else:
        return field[0] + radius - y


def index_to_xy(index):
    root = ceil(sqrt(index))
    radius = root // 2
    # Make sure it is an odd root
    root = root + 1 if root % 2 == 0 else root
    field = ((root - 2)**2, root**2)
    quadrant_size = (field[1] - field[0]) // 4
    quadrant = ((index - 1) - field[0]) // quadrant_size
    if quadrant == 0:
        offset = index - field[0]
        return (radius, radius - offset)
    if quadrant == 1:
        offset = index - field[0] - quadrant_size
        return (radius - offset, -radius)
    if quadrant == 2:
        offset = index - field[0] - 2 * quadrant_size
        return (-radius, -radius + offset)
    if quadrant == 3:
        offset = index - field[0] - 3 * quadrant_size
        return (-radius + offset, radius)


sums = {1: 1}
adjacent = (
        (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

n = 1
while sums.get(n) <= memory_square:
    n += 1
    x, y = index_to_xy(n)
    sums[n] = sum(sums.get(i, 0)
                  for i in starmap(xy_to_index, 
                                   ((option[0] + x, option[1] + y)
                                    for option in adjacent)))
print('First index with sum > {} is {}, with sum {}'.format(
      memory_square, n, sums.get(n)))

