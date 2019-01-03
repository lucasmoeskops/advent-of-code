from sys import argv


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

CLEAN = '.'
INFECTED = '#'

displacement = (0, -1), (1, 0), (0, 1), (-1, 0)

data = open(argv[1], 'r').read().strip().split('\n')

width, height = len(data[0]), len(data)
grid = {(x, y):val for y, line in enumerate(data) for x, val in enumerate(line)}

pos = width // 2, height // 2
direction = UP


def at(pos):
    return grid.get(pos, CLEAN)


def set(pos, value):
    grid[pos] = value


def move(pos, direction):
    return tuple(a + b for a, b in zip(pos, displacement[direction]))


def turn_left(direction):
    return (direction + 3) % 4


def turn_right(direction):
    return (direction + 1) % 4


def count_infected_nodes():
    return sum(1 for node in grid.values() if node == INFECTED)


def print_grid():
    min_x = min(key[0] for key in grid.keys())
    max_x = max(key[0] for key in grid.keys())
    min_y = min(key[1] for key in grid.keys())
    max_y = max(key[1] for key in grid.keys())
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(at((x, y)), end='')
        print('')


# Part 1

infections = 0
for burst in range(10000):
    if at(pos) == INFECTED:
        direction = turn_right(direction)
    else:
        direction = turn_left(direction)

    if at(pos) == CLEAN:
        set(pos, INFECTED)
        infections += 1
    else:
        set(pos, CLEAN)

    pos = move(pos, direction)

answer1 = infections 
print('After 10000 bursts there are {} infected nodes'.format(answer1))


# Part 2

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

depictions = '.', 'W', '#', 'F'

grid = {(x, y):depictions.index(val)
        for y, line in enumerate(data)
        for x, val in enumerate(line)}


def update(pos, value):
    grid[pos] = (value + 1) % 4


def write_grid():
    name = 'out_{}.txt'.format(argv[1])
    min_x = min(key[0] for key in grid.keys())
    max_x = max(key[0] for key in grid.keys())
    min_y = min(key[1] for key in grid.keys())
    max_y = max(key[1] for key in grid.keys())
    open(name, 'w').write(
            '\n'.join(
                ''.join(depictions[at((x, y))]
                        for x in range(min_x, max_x + 1))
                for y in range(min_y, max_y + 1)))


infections = 0
pos = width // 2, height // 2
direction = UP
for burst in range(1 * 10**7):
    if burst % 100000 == 0:
        print('{}%'.format(burst // 100000))

    value = at(pos)
    if value == CLEAN:
        direction = turn_left(direction)
    elif value == INFECTED:
        direction = turn_right(direction)
    elif value == FLAGGED:
        direction = turn_right(turn_right(direction))

    if value == WEAKENED:
        infections += 1

    update(pos, value)

    pos = move(pos, direction)

answer2 = infections 
print('After 10000000 bursts there are {} infected nodes'.format(answer2))
write_grid()

