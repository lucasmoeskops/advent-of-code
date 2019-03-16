from itertools import zip_longest
from os import path
from sys import argv


def is_aba(string):
    return all((
        len(string) == 3,
        string[0] == string[2],
        string[0] != string[1],
    ))

    
def is_abba(string):
    return all((
        len(string) == 4,
        string[0] == string[3],
        string[1] == string[2],
        string[0] != string[1],
    ))


def get_abas(string):
    for i in range(len(string) - 2):
        substring = string[i:i + 3]
        
        if is_aba(substring):
            yield substring


def has_abba(string):
    return any(is_abba(string[i:i + 4]) for i in range(len(string) - 3))


def reverse_aba(string):
    return string[1] + string[0] + string[1]


def supports_tls(ipv7):
    parts = tuple(composite.split('[') for composite in ipv7.split(']'))
    normals, hypernets = zip_longest(*parts, fillvalue=())
    return any(map(has_abba, normals)) and not any(map(has_abba, hypernets))


def supports_ssl(ipv7):
    parts = tuple(composite.split('[') for composite in ipv7.split(']'))
    normals, hypernets = tuple(zip_longest(*parts, fillvalue=()))
    return any(reverse_aba(aba) in hypernet for hypernet in hypernets
               for normal in normals for aba in get_abas(normal))


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    addresses = fp.read().strip().split('\n')

    part1 = len(tuple(filter(supports_tls, addresses)))
    part2 = len(tuple(filter(supports_ssl, addresses)))

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


