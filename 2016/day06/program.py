from collections import Counter
from os import path
from sys import argv


MOST_COMMON = 0
LEAST_COMMON = -1


def decode_message(message, method=MOST_COMMON):
    args = (1,) if method == MOST_COMMON else ()

    return ''.join(Counter(column).most_common(*args)[method][0]
                   for column in zip(*message))


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    contents = fp.read().strip().split('\n')

    part1 = decode_message(contents)
    part2 = decode_message(contents, method=LEAST_COMMON)

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


