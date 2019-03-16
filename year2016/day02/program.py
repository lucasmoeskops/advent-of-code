from os import path
from sys import argv


def find_position(instructions, start, is_valid=None):
    if is_valid is None:
        is_valid = lambda p: 0 <= p.real <= 2 and 0 <= p.imag <= 2

    position = start
    moves = {'U': -1j, 'R': 1, 'D': 1j, 'L': -1}

    for instruction in instructions:
        new = position + moves[instruction]
        if is_valid(new):
            position = new

    return position


def position_to_button(position):
    return str(int(position.real + position.imag * 3 + 1))


def position_to_actual_button(position):
    layout = '--1--' \
             '-234-' \
             '56789' \
             '-ABC-' \
             '--D--'

    offset = position + 2 + 2j
    return layout[int(offset.real + offset.imag * 5)]


def is_actual_layout_position(position):
    dx = abs(position.real)
    dy = abs(position.imag)
    return dx + dy <= 2


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    button_instructions = fp.read().strip().split('\n')

    position = 1 + 1j
    buttons = []

    for button_instruction in button_instructions:
        position = find_position(button_instruction, position)
        buttons.append(position_to_button(position))

    part1 = ''.join(buttons)
    
    position = -2
    actual_buttons = []

    for button_instruction in button_instructions:
        position = find_position(button_instruction, position,
                is_actual_layout_position)
        actual_buttons.append(position_to_actual_button(position))
    
    part2 = ''.join(actual_buttons)

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


