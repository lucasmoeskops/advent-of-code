from math import sqrt
from re import compile, match
from string import ascii_lowercase
from sys import argv

parser = compile(r'(?P<op>\w+) (?P<reg>\w)( (?P<val>-?\w+))?')
program = tuple(match(parser, line).groupdict()
                for line in open(argv[1], 'r').read().strip().split('\n'))


def resolve(state, variable):
    if variable in ascii_lowercase:
        return state['registers'].get(variable, 0)
    return int(variable)


def set(state, register, value):
    state['registers'][register] = resolve(state, value)


def add(state, register, value):
    state['registers'][register] = \
            resolve(state, register) + resolve(state, value)


def subtract(state, register, value):
    if state['gh_fix'] and register == 'h':
        is_prime = True
        b = resolve(state, 'b')
        for i in range(2, int(sqrt(b) + 1)):
            if b % i == 0:
                is_prime = False
        if not is_prime:
            state['registers'][register] = \
                    resolve(state, register) - resolve(state, value)
    else:
        state['registers'][register] = \
                resolve(state, register) - resolve(state, value)


def multiply(state, register, value):
    state['registers'][register] = \
            resolve(state, register) * resolve(state, value)
    state['mul_used'] += 1


def jump_not_zero(state, register, value):
    if state['gh_fix']:
        if resolve(state, register) != 0 \
                and (state['instruction_pointer'] > 27 or register != 'g'):
            state['instruction_pointer'] += resolve(state, value) - 1
    else:
        if resolve(state, register) != 0:
            state['instruction_pointer'] += resolve(state, value) - 1


op_map = {
    'set': set,
    'add': add,
    'sub': subtract,
    'mul': multiply,
    'jnz': jump_not_zero,
}


def run(*configurations):
    states = []

    for configuration in configurations:
        states.append({
            'program': configuration.get('instructions'),
            'id': configuration.get('id', 0),
            'instruction_pointer': 0,
            'mul_used': 0,
            'registers': {'p': configuration.get('id', 0)},
            'seen': {},
            'done': False,
            'gh_fix': configuration.get('gh_fix', False),
        })
        states[-1]['registers'].update(configuration.get('registers', {}))

    while any(not state['done'] for state in states):
        for state in states:
            if state['done']:
                continue

            ip = state['instruction_pointer']

            if len(states) == 1:
                # Break from infinite loops
                if ip not in state['seen']:
                    state['seen'][ip] = []
                elif state['registers'] in state['seen'][ip]:
                    state['done'] = True
                    break

                state['seen'][ip].append(state['registers'].copy())

            statement = state['program'][ip]

            op_map[statement['op']](state,
                                    statement['reg'],
                                    statement['val'])

            state['instruction_pointer'] += 1

            if not (0 <= state['instruction_pointer'] < len(state['program'])):
                state['done'] = True

    return states


# Part 1

state = run({'instructions': program})[0]
answer1 = state['mul_used']
print('The amount of times mul is used is {}'.format(answer1))


# Part 2

state = run({'instructions': program, 'gh_fix': True, 'registers': {'a': 1}})[0]
answer2 = state['registers']['h']
print('The final value of h is {}'.format(answer2))

