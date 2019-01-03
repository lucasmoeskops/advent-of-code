from itertools import count, repeat
from sys import argv

registers = tuple(int(x) for x in open(argv[1], 'r').read().strip().split('\t'))


# Part 1

registers1 = list(registers)
seen = set()
num = len(registers)
answer1 = 0
while tuple(registers1) not in seen:
    seen.add(tuple(registers1))
    redistribute = registers1.index(max(registers1))
    to_redistribute = zip(count(redistribute + 1),
                          repeat(1, registers1[redistribute]))
    registers1[redistribute] = 0
    for index, value in to_redistribute:
        registers1[index % num] += value
    answer1 += 1
print('Steps before a situation reoccurs: {}'.format(answer1))


# Part 2

registers1 = list(registers)
seen = set()
num = len(registers)
answer2 = 0
states = []
while tuple(registers1) not in seen:
    seen.add(tuple(registers1))
    states.append(tuple(registers1))
    redistribute = registers1.index(max(registers1))
    to_redistribute = zip(count(redistribute + 1),
                          repeat(1, registers1[redistribute]))
    registers1[redistribute] = 0
    for index, value in to_redistribute:
        registers1[index % num] += value
    answer2 += 1
print('Steps in a cycle: {}'.format(answer2 - states.index(tuple(registers1))))

