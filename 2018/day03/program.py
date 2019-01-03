from collections import Counter
from functools import reduce
from operator import itemgetter
from re import compile, match
from sys import argv

parser = compile(
        r'#(?P<ID>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<width>\d+)x(?P<height>\d+)')
data = tuple({k:int(v) for k, v in match(parser, line).groupdict().items()}
             for line in open(argv[1], 'r').read().strip().split('\n'))


# Part 1

extractable_data = map(itemgetter('x', 'y', 'width', 'height'), data)
claim_counter = Counter(
    (square_x, square_y)
    for x, y, width, height in extractable_data
    for square_x in range(x, x + width)
    for square_y in range(y, y + height))
answer1 = sum(1 for k, v in claim_counter.items() if v >= 2)
print('Square inches in two or more claims: {}'.format(answer1))


# Part 2

extractable_data = map(itemgetter('ID', 'x', 'y', 'width', 'height'), data)
isolated = (
    id
    for id, x, y, width, height in extractable_data
    if not any(
        claim_counter[(square_x, square_y)] > 1
        for square_x in range(x, x + width)
        for square_y in range(y, y + height)))
answer2 = next(isolated)
print('The only claim that doesn\'t overlap has ID {}'.format(answer2))

