from collections import defaultdict
from functools import reduce
from itertools import permutations
lines = open('input.txt', 'r').read().strip().split('\n')
distances = defaultdict(dict)
route_lengths = []
for line in lines:
    args = line.strip().split(' ')
    distances[args[0]][args[2]] = int(args[4])
    distances[args[2]][args[0]] = int(args[4])
for permutation in permutations(distances.keys(), len(distances)):
    route_lengths.append(reduce(
        lambda acc, point: (point, acc[1] + distances[acc[0]][point]),
        permutation[1:],
        (permutation[0], 0))[1])
print('The shortest route is {} miles.'.format(min(route_lengths)))
print('The longest route is {} miles.'.format(max(route_lengths)))
