from itertools import islice, takewhile
from os import path
from sys import argv


def not_parenthesis(char):
    return char not in ('(', ')')


def decompress(string):
    if string == '':
        return ''

    decompressed = []
    it = iter(string)
    
    while True:
        normal_data = ''.join(takewhile(not_parenthesis, it))
        decompressed.append(normal_data)
        pattern = ''.join(takewhile(not_parenthesis, it))
        
        if pattern:
            num_chars, replications = map(int, pattern.split('x'))
            decompressed.append(''.join(islice(it, num_chars)) * replications)
        elif not normal_data:
            break

    return ''.join(decompressed)


def decompressedv2_length(string):
    it = iter(string)
    length = 0

    while True:
        new_length = len(tuple(takewhile(not_parenthesis, it)))
        length += new_length
        pattern = ''.join(takewhile(not_parenthesis, it))
        
        if pattern:
            num_chars, replications = map(int, pattern.split('x'))
            replicated = ''.join(islice(it, num_chars))
            length += replications * decompressedv2_length(replicated)
        elif not new_length:
            break

    return length


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    compressed_data = fp.read().strip()

    part1 = len(decompress(compressed_data))
    part2 = decompressedv2_length(compressed_data)

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


