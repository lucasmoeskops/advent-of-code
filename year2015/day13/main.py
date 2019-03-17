from collections import defaultdict
from functools import reduce
from itertools import permutations
lines = open('input.txt', 'r').read().strip().split('\n')
happiness = defaultdict(dict)
sums = []
for line in lines:
    args = line.strip().split(' ')
    modifier = 1 if args[2] == 'gain' else -1
    happiness[args[0]][args[10].replace('.', '')] = modifier * int(args[3])
for permutation in permutations(happiness.keys(), len(happiness)):
    sums.append(reduce(
        lambda acc, person: (person,
                             acc[1]
                             + happiness[acc[0]][person]
                             + happiness[person][acc[0]]),
        permutation[1:] + (permutation[0],),
        (permutation[0], 0))[1])
print('The most achievable happiness is {}.'.format(max(sums)))
most_happiness = max(sums)
sums = []
for person in tuple(happiness):
    happiness['You'][person] = 0
    happiness[person]['You'] = 0
for permutation in permutations(happiness.keys(), len(happiness)):
    sums.append(reduce(
        lambda acc, person: (person,
                             acc[1]
                             + happiness[acc[0]][person]
                             + happiness[person][acc[0]]),
        permutation[1:] + (permutation[0],),
        (permutation[0], 0))[1])
print('The most achievable happiness of the actual guestlist is {}.'.format(
    max(sums)))
