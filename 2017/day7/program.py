from itertools import chain
from re import compile, match
from sys import argv

parser = compile(
    r'(?P<name>\w+) \((?P<weight>\d+)\)( -> (?P<subprograms>[\w, ]+))?$')
parsed  = tuple(match(parser, line).groupdict()
                for line in open(argv[1], 'r').read().strip().split('\n'))
programs = tuple({
    'name': data['name'],
    'weight': int(data['weight']),
    'subprograms': tuple(program.strip()
                         for program in data['subprograms'].split(', ')) \
                   if data['subprograms'] is not None else ()
    } for data in parsed)


# Part 1

subprograms = tuple(chain.from_iterable(program['subprograms']
                                        for program in programs))
answer1 = next(program['name']
               for program in programs if program['name'] not in subprograms)
print('The bottom of the tower is {}'.format(answer1))


# Part 2

def weight(program):
    return program['weight'] + \
           sum(weight(by_name[name]) for name in program['subprograms'])

def test(program):
    if program['name'] in adjustment:
        return adjustment[program['name']] == 0
    if not program['subprograms']:
        adjustment[program['name']] = 0
        return True
    for subprogram in program['subprograms']:
        if not test(by_name[subprogram]):
            return True
    sub_weights = tuple(weight(by_name[name])
                        for name in program['subprograms'])
    if sub_weights[0] == sub_weights[-1]:
        return True
    expected_weight = sorted(sub_weights)[len(program['subprograms']) // 2]
    for name in program['subprograms']:
        subprogram = by_name[name]
        program_weight = weight(subprogram)
        if program_weight != expected_weight:
            difference = expected_weight - program_weight
            adjustment[name] = subprogram['weight'] + difference
            subprogram['weight'] = adjustment[name]
        else:
            adjustment[name] = 0
    adjustment[program['name']] = 0
    return True


by_name = {program['name']:program for program in programs}
adjustment = {}
answer2 = None
answer2_program = None
for program in programs:
    if not test(program):
        answer2_program = program['name']
        answer2 = adjustment[program['name']]
print('The weight of program {} should be {}'.format(answer2_program, answer2))

