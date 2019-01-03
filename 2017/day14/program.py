from functools import reduce
from itertools import chain, cycle, islice, zip_longest
from sys import argv

keystring = argv[1] if len(argv) > 1 else 'oundnydw'


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def perform_round(elements, lengths, start, skip, size):
    position = start
    for length in lengths:
        until = position + length
        wrap = max(0, until - size)
        knot = tuple(islice(cycle(elements), position, until))[::-1]
        elements[position:until] = knot[0:length - wrap]
        elements[0:wrap] = knot[length - wrap:]
        position = (position + length + skip) % size
        skip += 1
    return position, skip


def knot_hash(to_hash, size=256):
    num_rounds = 64
    elements = list(range(size))
    lengths = tuple(chain(map(ord, to_hash), (17, 31, 73, 47, 23)))
    position = 0
    skip = 0
    for round in range(num_rounds):
        position, skip = perform_round(elements, lengths, position, skip, size)
    dense_hash = tuple(reduce(int.__xor__, group)
                       for group in grouper(elements, 16))
    return ''.join(hex(val)[2:].zfill(2) for val in dense_hash)


def hex_to_bin(hex_str):
    return ''.join(bin(int(char, 16))[2:].zfill(4) for char in hex_str)


def pop_adjacent(options, start, found=None):
    found = set() if found is None else found
    found.add(start)
    options.remove(start)
    for dx, dy in adjacent:
        position = (start[0] + dx, start[1] + dy)
        if position in options:
            pop_adjacent(options, position, found)
    return found


adjacent = (0, 1), (-1, 0), (0, -1), (1, 0)
knot_hashes = tuple(knot_hash('{}-{}'.format(keystring, i)) for i in range(128))


# Part 1

answer1 = sum(1
              for row in map(hex_to_bin, knot_hashes)
              for square in row
              if square == '1')
print('Total squares used is {}'.format(answer1))


# Part 2

used = set((x, y)
           for (y, row) in enumerate(map(hex_to_bin, knot_hashes))
           for (x, square) in enumerate(row)
           if square == '1')
groups = 0
while used:
    pop_adjacent(used, next(iter(used)))
    groups += 1
answer2 = groups
print('Number of groups in grid: {}'.format(answer2))

