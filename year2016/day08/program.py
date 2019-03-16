from os import path
from sys import argv
from time import sleep
from helpers import clear_terminal


class Screen:
    OFF = 0
    ON = 1

    def __init__(self, width=50, height=6):
        self.width = width
        self.height = height
        self.state = (Screen.OFF,) * self.width * self.height

    @property
    def lit_pixels(self):
        return sum(self.state)

    def representation(self):
        def pixel(i):
            return '#' if self.state[i] == Screen.ON else '.'

        def newline(i):
            return '\n' if (i + 1) % self.width == 0 else ''

        return ''.join(pixel(i) + newline(i) for i in range(len(self.state)))

    def rect(self, a, b):
        def in_rect(i):
            return i % self.width < a and i // self.width < b

        all_i = range(len(self.state))
        self.state = tuple(Screen.ON if in_rect(i) else self.state[i]
                           for i in all_i)

    def rotate_row_y(self, a, b):
        def in_row(i):
            return i // self.width == a

        def shift_right(i):
            return (i - b) % self.width + i // self.width * self.width

        all_i = range(len(self.state))
        self.state = tuple(self.state[shift_right(i) if in_row(i) else i]
                           for i in all_i)

    def rotate_column_x(self, a, b):
        def in_column(i):
            return i % self.width == a

        def shift_down(i):
            return (i - b * self.width) % (self.width * self.height)

        all_i = range(len(self.state))
        self.state = tuple(self.state[shift_down(i) if in_column(i) else i]
                           for i in all_i)


def execute_operations(screen, operations, simulate=False):
    for operation in operations:
        arguments = operation.split(' ')

        if arguments[0] == 'rect':
            screen.rect(*map(int, arguments[1].split('x')))
        elif arguments[0] == 'rotate':
            if arguments[1] == 'column':
                screen.rotate_column_x(int(arguments[2].split('=')[1]),
                                       int(arguments[4]))
            elif arguments[1] == 'row':
                screen.rotate_row_y(int(arguments[2].split('=')[1]),
                                    int(arguments[4]))
        else:
            print('Unknown operation {}'.format(arguments[0]))

        if simulate:
            clear_terminal()
            print(screen.representation())
            sleep(0.1)


def solve(fp=None, simulate=False, write=False):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    operations = fp.read().strip().split('\n')

    screen = Screen()
    execute_operations(screen, operations, simulate)

    part1 = screen.lit_pixels
    part2 = screen.representation() 

    if write:
        return 'Part 1 answer: {}\n\nPart 2 text:\n{}'.format(part1, part2)

    return (part1, part2)


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)
    kwargs['simulate'] = '-m' in argv and (argv.remove('-m') or True)
   
    kwargs['write'] = True

    if len(argv) > 1:
        kwargs['fp'] = open(argv[1], 'r')

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))

