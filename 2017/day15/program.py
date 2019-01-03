from re import compile, match
from sys import argv

parser = compile(r'Generator (?P<id>\w+) starts with (?P<value>\d+)')
a, b = (int(match(parser, line).groupdict()['value'])
        for line in open(argv[1], 'r').read().strip().split('\n'))


def generator(start, factor, constraint=None):
    value = start
    while True:
        value = value * factor % 2147483647
        if constraint is not None:
            while value % constraint != 0:
                value = value * factor % 2147483647
        yield value


# Part 1

gen_a = generator(a, 16807)
gen_b = generator(b, 48271)
total = 0
for i in range(4*10**1):
    if next(gen_a) & 0xffff == next(gen_b) & 0xffff:
        total += 1
print('Total pairs found: {}'.format(total))


# Part 2

gen_a = generator(a, 16807, 4)
gen_b = generator(b, 48271, 8)
total = 0
for i in range(5*10**6):
    if next(gen_a) & 0xffff == next(gen_b) & 0xffff:
        total += 1
print('Total pairs found: {}'.format(total))

