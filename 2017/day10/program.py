from functools import reduce
from itertools import chain, cycle, islice, zip_longest
from sys import argv

input_raw = open(argv[1], 'r').read().strip()
lengths = tuple(int(v) for v in input_raw.split(','))
size = int(argv[2] if len(argv) > 2 else 256)
input_raw = ' '.join(argv[3:]) if len(argv) > 3 else input_raw


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def perform_round(elements, lengths, start, skip):
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


# Part 1

elements = list(range(size))
perform_round(elements, lengths, 0, 0)
answer1 = int.__mul__(*elements[:2])
print('First two numbers multiplied is {}'.format(answer1))


# Part 2

num_rounds = 64
elements2 = list(range(size))
lengths2 = tuple(chain(map(ord, input_raw), (17, 31, 73, 47, 23)))
position2 = 0
skip2 = 0
for round in range(num_rounds):
    position2, skip2 = perform_round(elements2, lengths2, position2, skip2)
dense_hash = tuple(reduce(int.__xor__, group)
                   for group in grouper(elements2, 16))
answer2 = ''.join(hex(val)[2:].zfill(2) for val in dense_hash)
print('Final hash is {}'.format(answer2))

