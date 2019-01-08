from collections import Counter
from itertools import chain, islice, starmap
from operator import itemgetter
from os import path
from string import ascii_lowercase
from sys import argv


def parse_room(room_string):
    encrypted_name, rest = room_string.rsplit('-', 1)
    sector_id, checksum = rest.replace(']', '').split('[')
    return encrypted_name, int(sector_id), checksum


def is_valid_room(encrypted_name, checksum):
    occurrences = Counter(chain.from_iterable(encrypted_name.split('-')))
    return checksum == ''.join(islice(map(itemgetter(0),
                                          sorted(
                                              sorted(occurrences.most_common(),
                                                     key=itemgetter(0)),
                                              key=itemgetter(1),
                                              reverse=True)), 5))


def decipher(encrypted_name, sector_id):
    mod = sector_id % 26
    return ''.join(chr((ord(c) + mod - 97) % 26 + 97)
                   if c in ascii_lowercase else ' '
                   for c in encrypted_name)


def north_pole_filter(item):
    sector_id, name = item
    return 'north' in name or 'pole' in name


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    rooms = map(parse_room, fp.read().strip().split('\n'))
    valid_rooms = tuple((encrypted_name, sector_id)
                        for encrypted_name, sector_id, checksum in rooms
                        if is_valid_room(encrypted_name, checksum))

    part1 = sum(sector_id for encrypted_name, sector_id in valid_rooms)

    try:
        part2 = next(filter(north_pole_filter, 
                     zip(map(itemgetter(1), valid_rooms),
                         starmap(decipher, valid_rooms))))[0]
    except StopIteration:
        part2 = None

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


