from itertools import chain
from math import sqrt
from re import compile, match
from sys import argv


data = open(argv[1], 'r').read().strip().split('\n')
parser = compile(r'([#./]+) => ([#./]+)')
raw_rules = (match(parser, line).groups() for line in data)

rules = tuple((rule[0].replace('/', ''), rule[1].replace('/', ''))
              for rule in raw_rules)
grid = '.#.'\
       '..#'\
       '###'


class MutateException(Exception):
    pass


def operation(pattern, modifier):
    size = int(sqrt(len(pattern)))
    return ''.join(pattern[modifier(x, y)]
                   for x in range(size)
                   for y in range(size))


def rotate90(pattern):
    size = int(sqrt(len(pattern)))
    return operation(pattern, lambda x, y: size - y - 1 + x * size)


def rotate180(pattern):
    size = int(sqrt(len(pattern)))
    return operation(pattern, 
                     lambda x, y: (size - x - 1) + (size - y - 1) * size)


def rotate270(pattern):
    size = int(sqrt(len(pattern)))
    return operation(pattern, lambda x, y: y + (size - x - 1) * size)


def flip_horizontal(pattern):
    size = int(sqrt(len(pattern)))
    return operation(pattern, lambda x, y: (size - x - 1) + y * size)


def flip_vertical(pattern):
    size = int(sqrt(len(pattern)))
    return operation(pattern, lambda x, y: x + (size - y - 1) * size)


def count_on_pixels(grid):
    return sum(1 for pixel in grid if pixel == '#')


def cut_grid(grid):
    size = int(sqrt(len(grid)))
    split = 2 if size % 2 == 0 else 3
    return (''.join(grid[x + sx + (y + sy) * size] 
                    for sy in range(0, split)
                    for sx in range(0, split))
            for y in range(0, size, split)
            for x in range(0, size, split))


def sew_grid(pieces):
    pieces = tuple(pieces)
    piece_size = int(sqrt(len(pieces[0])))
    size = int(sqrt(len(pieces)))
    def piece_index(x, y):
        return x // piece_size + (y // piece_size) * size
    def pixel_index(x, y):
        return x % piece_size + y % piece_size * piece_size
    return ''.join(pieces[piece_index(x, y)][pixel_index(x, y)]
                   for y in range(0, size * piece_size)
                   for x in range(0, size * piece_size))


def write_grid(grid):
    name = 'out_{}.txt'.format(argv[1])
    size = int(sqrt(len(grid)))
    open(name, 'w').write('\n'.join(grid[y * size:(y + 1) * size]
                                    for y in range(size)))


def mutate(piece):
    for rule in extended_rules:
        if rule[0] == piece:
            return rule[1]
    raise MutateException('Couln\'t mutate') 


extended_rules = tuple(chain(
    rules,
    ((rotate90(rule[0]), rule[1]) for rule in rules),
    ((rotate180(rule[0]), rule[1]) for rule in rules),
    ((rotate270(rule[0]), rule[1]) for rule in rules),
    ((flip_horizontal(rule[0]), rule[1]) for rule in rules),
    ((flip_vertical(rule[0]), rule[1]) for rule in rules),
    ((rotate90(flip_vertical(rule[0])), rule[1]) for rule in rules),
))


# Part 1

iterations = 5
for iteration in range(iterations):
    try:
        grid = sew_grid(map(mutate, cut_grid(grid)))
    except:
        print('Couldn\'t mutate after iteration {}'.format(iteration))
        break

answer1 = count_on_pixels(grid)
print('Amount of on pixels: {}'.format(answer1))


# Part 2

iterations = 18
for iteration in range(iteration + 1, iterations):
    try:
        grid = sew_grid(map(mutate, cut_grid(grid)))
    except MutateException:
        print('Couldn\'t mutate after iteration {}'.format(iteration))
        break

answer2 = count_on_pixels(grid)
print('Amount of on pixels: {}'.format(answer2))
write_grid(grid)

