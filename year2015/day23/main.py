from sys import argv
from typing import NamedTuple, Optional


class Instruction(NamedTuple):
    type: str
    register: Optional[str] = None
    offset: Optional[int] = None


class Computer:
    def __init__(self, a=0, b=0):
        self.registers = {'a': a, 'b': b}
        self.instruction_pointer = 0

    def hlf(self, r):
        self.registers[r] //= 2
        self.instruction_pointer += 1

    def tpl(self, r):
        self.registers[r] *= 3
        self.instruction_pointer += 1

    def inc(self, r):
        self.registers[r] += 1
        self.instruction_pointer += 1

    def jmp(self, offset):
        self.instruction_pointer += offset

    def jie(self, r, offset):
        if self.registers[r] % 2:
            self.instruction_pointer += 1
        else:
            self.jmp(offset)

    def jio(self, r, offset):
        if self.registers[r] == 1:
            self.jmp(offset)
        else:
            self.instruction_pointer += 1


def parse_line(line):
    params = line.replace(',', '').split(' ')

    if '+' in params[1] or '-' in params[1]:
        return Instruction(params[0], offset=int(params[1]))
    elif len(params) > 2:
        return Instruction(params[0], params[1], int(params[2]))
    else:
        return Instruction(*params)


def run(computer):
    while 0 <= computer.instruction_pointer < len(instructions):
        instruction = instructions[computer.instruction_pointer]
        params = tuple(getattr(instruction, param)
                       for param in ('register', 'offset')
                       if getattr(instruction, param))
        getattr(computer, instruction.type)(*params)


lines = open('input.txt'
             if len(argv) < 2 else argv[1], 'r').read().strip().split('\n')
instructions = tuple(map(parse_line, lines))

computer = Computer()
run(computer)

value_in_b = computer.registers['b']
print(f'The value in register \'b\' when the computer is finished is'
      f' {value_in_b}.')


computer2 = Computer(1)
run(computer2)

value_in_b = computer2.registers['b']
print(f'The value in register \'b\' when the computer is finished if'
      f' \'a\' started as one is {value_in_b}.')
