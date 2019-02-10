from itertools import chain
from operator import attrgetter
from os import path
from sys import argv
from typing import Dict, Union, Optional, List

Parameter = Union[int, str]


class Computer:
    def __init__(self,
                 initialization: Optional[Dict[str, int]] = None,
                 speed_boost=True):
        self.registers: Dict[str, int] = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        if initialization:
            self.registers.update(initialization)
        self.instruction_pointer: int = 0
        self.speed_boost: bool = speed_boost

    def execute(self, program: 'Program'):
        self.instruction_pointer = 0
        while 0 <= self.instruction_pointer < len(program):
            if self.speed_boost:
                self._speed_up(program)
            self._execute_statement(program[self.instruction_pointer])
            self.instruction_pointer += 1

    def _speed_up(self, program: 'Program'):
        if self.instruction_pointer + 2 < len(program):
            i1: Statement = program[self.instruction_pointer]
            i2: Statement = program[self.instruction_pointer + 1]
            i3: Statement = program[self.instruction_pointer + 2]
            if i1.instruction == 'inc' \
                    and i2.instruction == 'dec' \
                    and i3.instruction == 'jnz'\
                    and i3.param2 == -2:
                self.registers[i1.param1] += self.registers[i2.param1]
                self.registers[i2.param1] = 0
                self.instruction_pointer += 2

    def _execute_statement(self, statement: 'Statement'):
        if statement.instruction == 'cpy':
            self.registers[statement.param2] = (
                statement.param1
                if isinstance(statement.param1, int)
                else self.registers[statement.param1])
        elif statement.instruction == 'inc':
            self.registers[statement.param1] += 1
        elif statement.instruction == 'dec':
            self.registers[statement.param1] -= 1
        elif statement.instruction == 'jnz':
            condition = (
                    0 != (statement.param1
                          if isinstance(statement.param1, int)
                          else self.registers[statement.param1]))
            if condition:
                self.instruction_pointer += (
                    statement.param2 - 1
                    if isinstance(statement.param2, int)
                    else self.registers[statement.param2] - 1)


class Program(list):
    pass


class Statement:
    def __init__(
            self,
            instruction: str,
            param1: Parameter,
            param2: Optional[Parameter] = None):
        self.instruction: str = instruction
        self.param1: Parameter = param1
        self.param2: Parameter = param2

    def __repr__(self):
        return ' '.join(
            chain(
                [self.instruction],
                *map(str, filter(None, (self.param1, self.param2)))))


def str_to_parameter(string: str) -> Parameter:
    return (
        int(string)
        if len(string) > 1 or abs(ord(string) - 53) < 5
        else string)


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    line: List[List] = [
        line.split(' ') for line in fp.read().strip().split('\n')]
    program = Program(Statement(argument[0],
                                *map(str_to_parameter, argument[1:]))
                      for argument in line)

    computer: Computer = Computer()
    computer.execute(program)

    computer2: Computer = Computer({'c': 1})
    computer2.execute(program)

    part1: int = computer.registers['a']
    part2: int = computer2.registers['a']

    return part1, part2


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


