from sys import argv

diagram = open(argv[1]).read().split('\n')[:-1]


def at(pos):
    if not (0 <= pos[0] < len(diagram[0]) and 0 <= pos[1] < len(diagram)):
        return ' '
    return diagram[pos[1]][pos[0]]

UP, RIGHT, DOWN, LEFT = (0, -1), (1, 0), (0, 1), (-1, 0)

def add(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])


def perpendicular_directions(direction):
    if direction in (UP, DOWN):
        return LEFT, RIGHT
    return UP, DOWN


# Part 1 & 2

pos = (diagram[0].index('|'), 0)
collected = []
bounds = (len(diagram[0]), len(diagram))
direction = DOWN
steps = 1
while 0 <= pos[0] < bounds[0] and 0 <= pos[1] < bounds[1]:
    if at(pos) == '+':
        for p_dir in perpendicular_directions(direction):
            if at(add(pos, p_dir)) != ' ':
                direction = p_dir
    if at(pos) not in ('+', '-', '|'):
        collected.append(at(pos))
    pos = add(pos, direction)
    if at(pos) == ' ':
        break
    steps += 1
answer1 = ''.join(collected)
answer2 = steps
print('The collected letters are, in order, {}'.format(answer1))
print('The number of steps travelled is {}'.format(answer2))

