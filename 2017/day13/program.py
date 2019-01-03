from operator import itemgetter
from re import compile, match
from sys import argv

parser = compile(r'(?P<depth>\d+): (?P<range>\d+)')
parsed = tuple(match(parser, line).groupdict()
               for line in open(argv[1], 'r').read().strip().split('\n'))
layers = {int(line['depth']):int(line['range']) for line in parsed}


def severity(depth):
    return layers[depth] * depth


def severity_after(delay):
    return sum(severity(depth)
               for depth in layers
               if ((depth + delay) % (2 * layers[depth] - 2) == 0))


# Part 1

answer1 = severity_after(0)
print('Severity of leaving immediately is {}'.format(answer1))


# Part 2
delay = 0
optimized = sorted(((depth, 2 * layers[depth] - 2) for depth in layers), 
                   key=itemgetter(1))
while True:
    for depth, roundtime in optimized:
        if (delay + depth) % roundtime == 0:
            delay += 1
            break
    else:
        break
answer2 = delay
print('Pass through after delay of {} picoseconds'.format(answer2))

