from operator import itemgetter
from re import compile, findall, match
from sys import argv

data = open(argv[1], 'r').read().strip()
data_lines = data.split('\n')
begin_state_parser = compile(r'Begin in state (\w+).')
checksum_after_parser = compile(
        r'Perform a diagnostic checksum after (\d+) steps.')
state_parser = compile(r'In state (\w+):\n(([^\n]|\n(?!\n))+)')
current_value_parser = compile(r'If the current value is (\d+):')
write_value_parser = compile(r'- Write the value (\d+).')
move_parser = compile(r'- Move one slot to the (left|right).')
continue_parser = compile(r'- Continue with state (\w+).')

begin_state = match(begin_state_parser, data_lines[0]).groups()[0]
checksum_after = int(match(checksum_after_parser, data_lines[1]).groups()[0])
raw_states = findall(state_parser, data)
states = {}

for raw_state in raw_states:
    name, data = raw_state[:2]
    state = {}
    lines = tuple(line.strip() for line in data.split('\n'))
    for i in range(0, len(lines), 4):
        state[int(match(current_value_parser, lines[i]).groups()[0])] = {
            'write': int(match(write_value_parser, lines[i + 1]).groups()[0]),
            'move': -1
                    if match(move_parser, lines[i + 2]).groups()[0] == 'left'
                    else 1,
            'continue': match(continue_parser, lines[i + 3]).groups()[0],
        }
    states[name] = state

tape = {}

def at(pos):
    return tape.get(pos, 0)


def set(pos, value):
    tape[pos] = value


# Part 1

state = begin_state
pos = 0
for i in range(checksum_after):
    value = at(pos)
    action = states[state][value]
    set(pos, action['write'])
    pos += action['move']
    state = action['continue']
answer1 = sum(1 for value in tape.values() if value == 1)
print('Checksum is {}'.format(answer1))

