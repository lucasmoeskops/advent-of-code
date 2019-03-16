from sys import argv


def get_checksum(disc_size, data):
    while len(data) < disc_size:
        data += '0' + ''.join('1' if c == '0' else '0' for c in data[::-1])
    data = data[:disc_size]

    while len(data) % 2 == 0:
        data = ''.join('1' if data[i] == data[i + 1] else '0' for i in
                       range(0, len(data), 2))
    return data


def fast_get_checksum(disc_size, data):
    def at(index):
        index %= m
        if index < l:
            return data[index]
        if index == l:
            pass
        if index == m - 1:
            pass
        return data[m - index]
    l = len(data)
    data += 'X' + ''.join('1' if c == '0' else '0' for c in data[::-1])
    m = len(data) + 1

    t = disc_size
    while t % 2 == 0:
        checksum = ''.join('1' if at[i] == at[i + 1] else '0' for i in
                       range(0, len(disc_size), 2))
        t /= 2
    return checksum


def solve(disc_size=272, initial='01111001100111011', disc_size_2=35651584):
    part1: str = get_checksum(disc_size, initial)
    part2: int = get_checksum(disc_size_2, initial)

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['disc_size'] = int(argv[1])

    if len(argv) > 2:
        kwargs['initial'] = str(argv[2])

    if len(argv) > 3:
        kwargs['disc_size_2'] = str(argv[3])

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


