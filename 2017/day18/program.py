from re import compile, match
from string import ascii_lowercase
from sys import argv

parser = compile(r'(?P<op>\w+) (?P<reg>\w)( (?P<val>-?\w+))?')
program = tuple(match(parser, line).groupdict()
                for line in open(argv[1], 'r').read().strip().split('\n'))


class ReceiveDeadlock(Exception):
    pass


def resolve(state, variable):
    if variable in ascii_lowercase:
        return state['registers'].get(variable, 0)
    return int(variable)


def play_sound(state, register):
    state['last_played_sound'] = resolve(state, register)


def set(state, register, value):
    state['registers'][register] = resolve(state, value)


def add(state, register, value):
    state['registers'][register] = \
            resolve(state, register) + resolve(state, value)


def multiply(state, register, value):
    state['registers'][register] = \
            resolve(state, register) * resolve(state, value)


def modulo(state, register, value):
    state['registers'][register] = \
            resolve(state, register) % resolve(state, value)


def recover(state, register):
    if resolve(state, register) != 0:
        state['recovers'].append(state['last_played_sound'])


def jump_greater_zero(state, register, value):
    if resolve(state, register) > 0:
        state['instruction_pointer'] += resolve(state, value) - 1


def send(state, register):
    state['send_buffer'].append(resolve(state, register))
    state['values_sent'] += 1


def receive(state, register):
    try:
        state['registers'][register] = state['receive_buffer'].pop(0)
    except IndexError:
        raise ReceiveDeadlock


op_map = {
    'snd': lambda *args: play_sound(*args[:-1]),
    'set': set,
    'add': add,
    'mul': multiply,
    'mod': modulo,
    'rcv': lambda *args: recover(*args[:-1]),
    'jgz': jump_greater_zero,
}


def run(*configurations):
    states = []

    for configuration in configurations:
        states.append({
            'program': configuration.get('instructions'),
            'id': configuration.get('id', 0),
            'instruction_pointer': 0,
            'last_played_sound': None,
            'recovers': [],
            'registers': {'p': configuration.get('id', 0)},
            'seen': {},
            'send_buffer': configuration.get('send_buffer'),
            'receive_buffer': configuration.get('receive_buffer'),
            'done': False,
            'waiting': False,
            'values_sent': 0,
        })

    while any(not state['waiting'] and not state['done'] for state in states):
        for state in states:
            if state['done']:
                continue

            ip = state['instruction_pointer']

            if len(states) == 1:
                # Just to break from the program in part 1
                if ip not in state['seen']:
                    state['seen'][ip] = []
                elif state['registers'] in state['seen'][ip]:
                    state['done'] = True
                    break

                state['seen'][ip].append(state['registers'].copy())

            statement = state['program'][ip]

            try:
                op_map[statement['op']](state,
                                        statement['reg'],
                                        statement['val'])
            except ReceiveDeadlock:
                state['waiting'] = True
            else:
                if state['waiting']:
                    state['waiting'] = False

                state['instruction_pointer'] += 1

            if not (0 <= state['instruction_pointer'] < len(state['program'])):
                state['done'] = True

    return states


# Part 1

state = run({'instructions': program})[0]
answer1 = state['recovers'][0]
print('The value of the first recover is {}'.format(answer1))


# Part 2

op_map['rcv'] = lambda *args: receive(*args[:-1])
op_map['snd'] = lambda *args: send(*args[:-1])
p0_send = []
p1_send = []
states = run({
    'id': 0,
    'instructions': program,
    'send_buffer': p0_send,
    'receive_buffer': p1_send
}, {
    'id': 1,
    'instructions': program,
    'send_buffer': p1_send,
    'receive_buffer': p0_send,
})
answer2 = states[1]['values_sent']
print('Program 1 sent {} values'.format(answer2))

