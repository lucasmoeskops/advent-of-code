from functools import reduce
from hashlib import md5
from sys import argv


directions = -1j, 1j, -1, 1
direction_names = 'U', 'D', 'L', 'R'


def get_directions(code):
    def is_open(char):
        return ord('b') <= ord(char) <= ord('f')
    return tuple(map(is_open, md5(code.encode('utf-8')).hexdigest()[:4]))


def recurse(position, code, path_chooser):
    options = get_directions(code)
    paths = []
    if position == 3+3j:
        return ''
    for possible, direction, name in zip(options, directions, direction_names):
        if (possible and 0 <= (position + direction).imag < 4
                and 0 <= (position + direction).real < 4):
            follow = recurse(position + direction, code + name, path_chooser)
            if follow is not None:
                paths.append(name + follow)
    paths = tuple(filter(None, paths))
    return path_chooser(paths) if paths else None


def solve(pass_code='gdjjyniy'):
    def choose_shortest(paths):
        return reduce(lambda a, b: a if len(a) < len(b) else b, paths)
    def choose_longest(paths):
        return reduce(lambda a, b: a if len(a) > len(b) else b, paths)
    part1: str = recurse(0+0j, pass_code, choose_shortest)
    part2: str = len(recurse(0+0j, pass_code, choose_longest))

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['pass_code'] = argv[1]

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


