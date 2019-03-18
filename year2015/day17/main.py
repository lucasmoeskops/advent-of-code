from itertools import combinations
containers = tuple(map(int, open('input.txt', 'r').read().strip().split('\n')))
combos = 0
for i in range(1, len(containers) + 1):
    for combination in combinations(containers, i):
        if sum(combination) == 150:
            combos += 1
print('There are {} different combinations.'.format(combos))
for i in range(1, len(containers) + 1):
    combos = 0
    for combination in combinations(containers, i):
        if sum(combination) == 150:
            combos += 1
    if combos:
        break
print('There are {} ways to fill the containers with the minimum number of'
      ' containers required.'.format(combos))
