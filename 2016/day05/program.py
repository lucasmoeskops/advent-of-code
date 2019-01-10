from hashlib import md5
from itertools import count, dropwhile
from os import path, system
from random import choice
from sys import argv, stdout
from termcolor import colored


def calculate_password(door_id):
    def get_hash(index):
        return md5(bdoor_id + str(index).encode('utf-8')).hexdigest()

    def invalid_index(index):
        return get_hash(index)[:5] != '00000'

    bdoor_id = door_id.encode('utf-8')
    counter = count()

    return ''.join(get_hash(next(dropwhile(invalid_index, counter)))[5]
                   for i in range(8))


def calculate_password_2_animated(door_id):
    def get_hash(index):
        return md5(bdoor_id + str(index).encode('utf-8')).hexdigest()

    def invalid_index(index):
        h = get_hash(index)
        return h[:5] != '00000' or ord(h[5]) > ubound \
               or password[int(h[5])] != '_'

    def print_password():
        nonlocal found

        print('\b' * 8, end='')

        for i in range(8):
            if password[i] == '_':
                print(colored(choice('123456789abcdef'), 'green'), end='')
            else:
                print(colored(password[i], 'green'), end='')

        stdout.flush()

    def animated_check(index):
        if index % speed == 0:
            print_password()

        return invalid_index(index)

    def update_password(hash_):
        nonlocal found, speed

        password[int(hash_[5])] = hash_[6]
        found += 1
        speed = base_speed - base_speed // (9 - found)
        print_password()

    print('')
    print('_' * 8, end='')

    bdoor_id = door_id.encode('utf-8')
    ubound = ord('7')
    counter = count()
    password = ['_'] * 8
    found = 0
    base_speed = 25000
    speed = base_speed
    
    for i in range(8):
        update_password(get_hash(next(dropwhile(animated_check, counter))))

    print('')
    return password

def solve(door_id='reyedfim', only_part_2=False):
    part1 = None

    if not only_part_2:
        part1 = calculate_password(door_id) 

    part2 = calculate_password_2_animated(door_id)

    return (part1, part2)


if __name__ == '__main__':
    kwargs = {}

    tostdout = '-s' in argv and (argv.remove('-s') or True)
    only2 = '-2' in argv and (argv.remove('-2') or True)

    kwargs['only_part_2'] = only2
    
    if len(argv) > 1:
        kwargs['door_id'] = argv[1]

    solution = solve(**kwargs)

    if tostdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


