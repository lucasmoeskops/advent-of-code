from string import ascii_lowercase
from sys import argv

moves = open(argv[1], 'r').read().strip().split(',')
size = int(argv[2]) if len(argv) > 2 else 16


def perform_dance():
    global programs
    for move in moves:
        if move[0] == 's':
            amount = int(move[1:])
            programs = programs[-amount:] + programs[:-amount]
        elif move[0] == 'x':
            p, q = map(int, move[1:].split('/'))
            x = programs[p]
            programs[p] = programs[q]
            programs[q] = x
        elif move[0] == 'p':
            p, q = (programs.index(x) for x in move[1:].split('/'))
            x = programs[p]
            programs[p] = programs[q]
            programs[q] = x

# Part 1

programs = [x for x in ascii_lowercase[:size]]

perform_dance()
answer1 = ''.join(programs)
print('The order of the programs is {}'.format(answer1))


# Part 2

programs = [x for x in ascii_lowercase[:size]]
seen = []
while ''.join(programs) not in seen:
    seen.append(''.join(programs))
    perform_dance()
cycle = len(seen) - seen.index(''.join(programs)) 
offset = len(seen) - cycle
answer2 = ''.join(seen[(1*10**9 - offset) % cycle])
print('After 1 billion dances, the order is: {}'.format(answer2))

