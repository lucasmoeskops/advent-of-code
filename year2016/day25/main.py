from itertools import cycle
from os import path
from sys import argv

from year2016.day23.main import HQComputer, parse_program


class HQRoofComputer(HQComputer):
    def execute(self, program: 'Program'):
        self.program = program
        super().execute(program)

    def execute(self, program: 'Program'):
        self.instruction_pointer = 0
        while 0 <= self.instruction_pointer < len(program):
            if self.speed_boost:
                self._speed_up(program)
            r = self._execute_statement(program[self.instruction_pointer])
            if r is not None:
                yield r
            self.instruction_pointer += 1

    def _execute_statement(self, statement: 'TogglableStatement'):
        if statement.instruction == 'out':
            return (statement.param1 if isinstance(statement.param1, int) else
                    self.registers[statement.param1])
        super()._execute_statement(statement)


def find_correct_a(program):
    a = 0
    max_i = 0
    while True:
        computer = HQRoofComputer({'a': a})
        expect = cycle((0, 1))
        i = 0
        correct_a = False
        for value in computer.execute(program):
            if i > max_i:
                max_i = i
            if value != next(expect):
                a += 1
                break
            if i > 100:
                correct_a = True
                break
            i += 1
        if correct_a:
            return a


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    data = fp.read().strip().split('\n')
    program = parse_program(data)

    part1 = find_correct_a(program)
    part2 = None

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['fp'] = open(argv[1])

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


