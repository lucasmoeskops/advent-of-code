from itertools import cycle, islice
from operator import itemgetter
from os import path
from sys import argv


def scramble(password, operation_list, unscramble=False):
    password = list(password)
    for operation in operation_list[::-1 if unscramble else 1]:
        if operation.startswith('swap position'):
            a, b = map(int, itemgetter(2, 5)(operation.split(' ')))
            t = password[a]
            password[a] = password[b]
            password[b] = t
        elif operation.startswith('swap letter'):
            a, b = itemgetter(2, 5)(operation.split(' '))
            password = ''.join(password)
            password = password.replace(a, '$')
            password = password.replace(b, a)
            password = password.replace('$', b)
            password = list(password)
        elif operation.startswith('reverse positions'):
            a, b = map(int, itemgetter(2, 4)(operation.split(' ')))
            password[a:b+1] = password[a:b+1][::-1]
        elif operation.startswith(
                'rotate ' + ('right' if unscramble else 'left')):
            a = int(itemgetter(2)(operation.split(' ')))
            password = (password + password)[a:len(password) + a]
        elif operation.startswith(
                'rotate ' + ('left' if unscramble else 'right')):
            a = int(itemgetter(2)(operation.split(' ')))
            if a != 0:
                password = (password + password)[len(password)-a:-a]
        elif operation.startswith('rotate based on position of letter'):
            a = itemgetter(6)(operation.split(' '))
            i = password.index(a)
            if unscramble:
                for i in range(len(password)):
                    if scramble(''.join(password),
                                ['rotate left {} steps'.format(i),
                                'rotate based on position of letter {}'
                                        .format(a)]) == ''.join(password):
                        password = list(scramble(''.join(password), [
                            'rotate left {} steps'.format(i)]))
                        break
            else:
                r = (i + 1 + (1 if i >= 4 else 0)) % len(password)
                password = list(islice(cycle(password), len(password) - r,
                                       2 * len(password) - r))
        elif operation.startswith('move position'):
            a, b = map(int, itemgetter(2, 5)(operation.split(' ')))
            if unscramble:
                t = a
                a = b
                b = t
            c = password[a]
            password.pop(a)
            password.insert(b, c)
    return ''.join(password)


def solve(fp=None, password='abcdefgh', password_2='fbgdceah'):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    operations = fp.read().strip().split('\n')

    part1: str = scramble(password, operations)
    part2: str = scramble(password_2, operations, unscramble=True)

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['fp'] = open(argv[1])

    if len(argv) > 2:
        kwargs['password'] = argv[2]
    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


