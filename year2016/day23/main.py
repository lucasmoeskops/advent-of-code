from os import path
from sys import argv
from typing import List

from year2016.day12.main import Computer, Statement, Program, str_to_parameter


class HQComputer(Computer):
    def execute(self, program: 'Program'):
        self.program = program
        super().execute(program)

    def _execute_statement(self, statement: 'TogglableStatement'):
        if statement.instruction == 'tgl':
            skip = (statement.param1 if isinstance(statement.param1, int)
                    else self.registers[statement.param1])
            if 0 <= self.instruction_pointer + skip < len(self.program):
                self.program[self.instruction_pointer + skip].toggle()
        else:
            super()._execute_statement(statement)

    def _speed_up(self, program: 'Program'):
        if self.instruction_pointer + 5 < len(program):
            i1: Statement = program[self.instruction_pointer]
            i2: Statement = program[self.instruction_pointer + 1]
            i3: Statement = program[self.instruction_pointer + 2]
            i4: Statement = program[self.instruction_pointer + 3]
            i5: Statement = program[self.instruction_pointer + 4]
            i6: Statement = program[self.instruction_pointer + 5]
            if i1.instruction == 'cpy' and i1.param2 == i3.param1 \
                    and i2.instruction == 'inc' \
                    and i3.instruction == 'dec' and i3.param1 == i4.param1 \
                    and i4.instruction == 'jnz' \
                    and i5.instruction == 'dec' \
                    and i6.instruction == 'jnz' \
                    and i6.param2 == -5 and i6.param1 == i5.param1:
                v = i1.param1 if isinstance(i1.param1, int) else \
                    self.registers[i1.param1]
                v2 = i5.param1 if isinstance(i5.param1, int) else \
                    self.registers[i5.param1]
                self.registers[i2.param1] += v * v2
                self.registers[i3.param1] = 0
                self.registers[i6.param1] = 0
                self.instruction_pointer += 5
        super()._speed_up(program)


class TogglableStatement(Statement):
    def toggle(self):
        if self.instruction == 'inc':
            self.instruction = 'dec'
        elif self.instruction in ('dec', 'tgl'):
            self.instruction = 'inc'
        elif self.instruction == 'jnz':
            self.instruction = 'cpy'
        elif self.instruction in ('cpy',):
            self.instruction = 'jnz'
        else:
            raise RuntimeError('Don\'t know how to toggle {}'.format(
                self.instruction))


def parse_program(lines):
    line: List[List] = [line.split(' ') for line in lines]
    return Program(TogglableStatement(argument[0],
                                      *map(str_to_parameter, argument[1:]))
                   for argument in line)


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    data = fp.read().strip().split('\n')

    program = parse_program(data)
    computer = HQComputer({'a': 7})
    computer.execute(program)
    program2 = parse_program(data)
    computer2 = HQComputer({'a': 12})
    computer2.execute(program2)

    part1 = computer.registers['a']
    part2 = computer2.registers['a']

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


