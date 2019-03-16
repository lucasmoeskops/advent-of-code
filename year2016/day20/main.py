from operator import itemgetter
from os import path
from sys import argv


def find_lowest_unblocked(ban_list):
    lowest = 0
    while True:
        for ban_from, ban_until in ban_list:
            if lowest in range(ban_from, ban_until):
                lowest = ban_until + 1
                break
        else:
            return lowest


def find_num_allowed(ban_list):
    allowed = 0
    lowest = 0
    max_ip = 4294967295
    relevant_filters = ban_list
    while True:
        for ban_from, ban_until in relevant_filters:
            if lowest in range(ban_from, ban_until):
                lowest = ban_until + 1
                break
        else:
            relevant_filters = tuple(filter(lambda t: t[0] > lowest,
                                            ban_list))
            if not relevant_filters:
                allowed += max(0, max_ip + 1 - lowest)
                break
            lowest_filter = min(relevant_filters, key=itemgetter(0))
            allowed += lowest_filter[0] - lowest
            lowest = lowest_filter[1] + 1
    return allowed


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    ban_list = tuple(tuple(map(int, line.split('-'))) for line in fp.read(
        ).strip().split('\n'))

    part1: str = find_lowest_unblocked(ban_list)
    part2: str = find_num_allowed(ban_list)

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['fp'] = int(argv[1])

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


