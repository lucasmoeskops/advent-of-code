from os import path
from sys import argv


LEFT = -1
RIGHT = 1


def change_face(face, direction):
    """ left = 0, right = 1 """
    return complex(face.imag * -direction, face.real * direction)


def positions(route):
    position = 0
    face = -1j
    it = iter(route)
    positions = []
    
    while True:
        try:
            line = next(it)
        except StopIteration:
           break 

        direction = line[0]
        steps = int(line[1:])

        face = change_face(face, RIGHT if direction == 'R' else LEFT)
        for i in range(steps):
            position += face
            positions.append(position)

    return tuple(positions)


def determine_distance(position):
    return int(abs(position.imag) + abs(position.real))


def first_revisited_location(route):
    it = iter(route)
    visited = set()
    positions_ = positions(route)

    for position in positions_:
        if position in visited:
            return position

        visited.add(position)
    

def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    route = tuple(item.strip() for item in fp.read().split(','))

    part1 = determine_distance(positions(route)[-1])

    try:
        part2 = determine_distance(first_revisited_location(route))
    except AttributeError:
        part2 = None

    return (part1, part2)


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)
    
    if len(argv) > 1:
        kwargs['fp'] = open(argv[1], 'r')

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))

