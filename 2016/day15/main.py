import re
from sys import argv
from os import path


def mod_index(a, b, m, n):
    """ Find a solution to (m + k * a) === n mod b assuming gcd(a, b) == 1 """
    for k in range(b):
        if (m + a * k) % b == n:
            return k


class Disc:
    def __init__(self, positions: int, start: int, number: int):
        self.positions = positions
        self.offset = start + number


def solver(discs):
    offset = 0
    period = 1
    for disc in discs:
        p = disc.positions
        o = disc.offset
        k = mod_index(period, p, offset, (p - o) % p)
        offset += k * period
        period *= p
    return offset % period


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    parser = re.compile(r'Disc #(?P<number>\d+) has (?P<positions>\d+) '
                        r'positions; at time=0, it is at position ('
                        r'?P<start>\d+).')
    discs = [Disc(**{k: int(v) for k, v in parser.match(line.strip(
        )).groupdict().items()}) for line in fp.read().strip().split('\n')]

    part1: int = solver(discs)
    part2: int = solver(discs + [Disc(11, 0, len(discs) + 1)])

    return part1, part2


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


