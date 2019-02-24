from sys import argv


def play_game(elves, start=1, skip=1):
    if elves == 1:
        return start
    if elves % 2 == 0:
        return play_game(elves // 2, start, skip * 2)
    else:
        return play_game(elves // 2, start + skip * 2, skip * 2)


def play_variation(elves):
    j = 1
    while 5 + 6 * j <= elves:
        j = 3 * j + 1
    j = ((j - 1) // 3) * 6 + 3
    k = 1
    while 5 + 12 * k <= elves:
        k = 3 * k + 1
    k = ((k - 1) // 3) * 12 + 5
    if elves <= k or k <= j:
        return elves - j
    return (elves - k) * 2 + k // 2 - 1


def solve(elves=3017957):

    part1: str = play_game(elves)
    part2: str = play_variation(elves)

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['elves'] = int(argv[1])

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


