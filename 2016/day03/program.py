from helpers import grouper
from itertools import chain, permutations, starmap, tee
from os import path
from sys import argv


def is_valid_triangle(side1, side2, side3):
    return all(a + b > c for a, b, c in permutations((side1, side2, side3), 3))


def altsplit(triangles):
    return chain.from_iterable(zip(*group) for group in grouper(triangles, 3))


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    triangles = (tuple(int(value.strip())
                       for value in filter(None, line.strip().split(' ')))
                 for line in fp.read().strip().split('\n'))

    tri1, tri2 = tee(triangles, 2)

    part1 = sum(1
                for is_valid in starmap(is_valid_triangle, tri1)
                if is_valid)

    try:
        new_triangles = altsplit(tri2)

        part2 = sum(1
                    for is_valid in starmap(is_valid_triangle, new_triangles)
                    if is_valid)
    except TypeError:
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


