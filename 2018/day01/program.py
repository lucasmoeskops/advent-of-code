from itertools import accumulate, cycle
from sys import argv

frequencies = tuple(map(int, open(argv[1], 'r').read().split('\n')[:-1]))


# Part 1

answer1 = sum(frequencies)
print('Frequency sum is: {}'.format(answer1))


# Part 2

seen = {0}
answer2 = None
generator = accumulate(cycle(frequencies))

while True:
    new = next(generator)

    if new in seen:
        answer2 = new
        break

    seen.add(new)

print('First frequency seen twice is: {}'.format(answer2))


# Bonus information

print('Frequencies seen before reoccurrence: {}'.format(len(seen)))

