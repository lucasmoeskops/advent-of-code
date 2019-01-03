from itertools import chain
from sys import argv

data = open(argv[1], 'r').read().strip().split('\n')
parts = tuple(tuple(map(int, line.split('/'))) for line in data)


LEFT = 0
RIGHT = 1


def recursive_fit(current_part, parts_left, match=RIGHT):
    if not current_part:
        current_part = (0, 0)

    if not parts_left:
        return sum(current_part), ()

    max_strength = 0
    max_parts = ()
    for part in parts_left:
        match_at = False
        if part[LEFT] == current_part[match]:
            match_at = RIGHT
        if part[RIGHT] == current_part[match]:
            match_at = LEFT
        if match_at is not False:
            strength, parts = recursive_fit(part,
                                            parts_left - {part},
                                            match_at)
            if strength > max_strength:
                max_strength = strength
                max_parts = chain(parts)
    return max_strength + sum(current_part), chain((current_part,), max_parts)


def recursive_fit2(current_part, parts_left, match=RIGHT):
    if not current_part:
        current_part = (0, 0)

    if not parts_left:
        return sum(current_part), ()

    max_strength = 0
    max_parts = ()
    for part in parts_left:
        match_at = False
        if part[LEFT] == current_part[match]:
            match_at = RIGHT
        if part[RIGHT] == current_part[match]:
            match_at = LEFT
        if match_at is not False:
            strength, parts = recursive_fit2(part,
                                             parts_left - {part},
                                             match_at)
            if (len(parts) == len(max_parts) and strength > max_strength) \
                    or len(parts) > len(max_parts):
                max_strength = strength
                max_parts = parts
    return max_strength + sum(current_part), (current_part,) + max_parts


# Part 1

answer1, bridge_parts = recursive_fit((0, 0), set(parts))
print('Largest possible bridge has strength {}'.format(answer1))


# Part 2

answer2, bridge_parts = recursive_fit2((0, 0), set(parts))
print('Longest then strongest possible bridge has strength {}'.format(answer2))

