from re import compile, match
from sys import argv

parser = compile(r'(?P<reg>\w+) (?P<op>\w+) (?P<val>-?\d+) '
                  'if (?P<lcon>\w+) (?P<cmp>[^ ]+) (?P<rcon>-?\d+)')
parsed_lines = (match(parser, line).groupdict()
                for line in open(argv[1], 'r').read().strip().split('\n'))
instructions = tuple({
    'reg': line['reg'],
    'op': line['op'],
    'val': int(line['val']),
    'lcon': line['lcon'],
    'cmp': line['cmp'],
    'rcon': int(line['rcon']),
} for line in parsed_lines)

ops = {
    'inc': lambda a, b: a + b,
    'dec': lambda a, b: a - b,
}

cmps = {
    '!=': lambda a, b: a != b,
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
    '==': lambda a, b: a == b,
}

# Part 1 & 2

registers = {instruction['reg']:0 for instruction in instructions}
max_value = 0
for instruction in instructions:
    cmp = cmps[instruction['cmp']]
    op = ops[instruction['op']]
    register = instruction['reg']
    if cmp(registers[instruction['lcon']], instruction['rcon']):
        registers[register] = op(registers[register], instruction['val'])
        max_value = max(registers[register], max_value)
answer1 = max(registers.values())
answer2 = max_value
print('The largest value in any register is {}'.format(answer1))
print('The largest value held during the process is {}'.format(answer2))
