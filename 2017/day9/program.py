from re import compile, match, sub
from sys import argv

stream = open(argv[1], 'r').read().strip()


# Part 1 & 2

MODE_GARBAGE = 1
MODE_GROUP = 2

stream1 = sub(r'!.', '', stream)
score = 0
depth = 1
mode = MODE_GROUP
garbage_removed = 0
for char in stream1:
    if mode == MODE_GARBAGE:
        if char == '>':
            mode = MODE_GROUP
        else:
            garbage_removed += 1
    else:
        if char == '<':
            mode = MODE_GARBAGE
        elif char == '{':
            score += depth
            depth += 1
        elif char == '}':
            depth -= 1
answer1 = score
answer2 = garbage_removed
print('Group score is {}'.format(answer1))
print('Garbage removed is {}'.format(answer2))
