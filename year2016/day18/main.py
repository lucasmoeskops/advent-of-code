from io import StringIO
from os import path
from sys import argv


SAFE = '.'
TRAP = '^'


def calculate_row(previous_row):
    previous_row = SAFE + previous_row + SAFE
    return ''.join(TRAP if a != b else SAFE for a, b in zip(previous_row[:-2],
                                                            previous_row[2:]))


def get_rows(n, first_row):
    rows = [first_row]
    for i in range(n - 1):
        rows.append(calculate_row(rows[i]))
    return rows


def brute_force(first_row, rows):
    row = [char == '.' for char in first_row]
    rows -= 1
    safe_count = sum(1 for char in row if char)
    while rows:
        row = [row[1]] + [a == b for a, b in zip(row, row[2:])] + [row[-2]]
        safe_count += sum(1 for char in row if char)
        rows -= 1
    return safe_count


def solve(fp=None, rows=40, rows_2=400000):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    first_row = fp.read().strip()

    part1: str = brute_force(first_row, rows)
    part2: str = brute_force(first_row, rows_2)

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['rows'] = int(argv[1])

    if len(argv) > 2:
        if '^' in argv[2]:
            kwargs['fp'] = StringIO(argv[2])
        else:
            kwargs['fp'] = open(argv[2], 'r')

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


