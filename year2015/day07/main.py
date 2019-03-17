from collections import defaultdict
from string import ascii_lowercase
instructions = open('input.txt', 'r').read().strip().split('\n')
s = 2**16
registers = {}
waiting_for = defaultdict(list)
dependencies = defaultdict(list)
operators = {
    'SET': lambda x: x % s,
    'AND': lambda x, y: (x & y) % s,
    'RSHIFT': lambda x, y: (x >> y) % s,
    'OR': lambda x, y: (x | y) % s,
    'NOT': lambda x: (~x) %s,
    'LSHIFT': lambda x, y: (x << y) % s,
}
def convert(inp):
    return registers.get(inp, 0) if inp[0] in ascii_lowercase else int(inp)
def check_parameter(p):
    if p[0] not in ascii_lowercase:
        registers[p] = int(p)
    if isinstance(registers.get(p), int):
        for register in waiting_for[p]:
            if p in dependencies[register]:
                dependencies[register].remove(p)
                if not dependencies[register]:
                    val = registers[register]
                    if len(val) == 1:
                        registers[register] = convert(val[0])
                    elif len(val) == 2:
                        registers[register] = val[0](convert(val[1]))
                    else:
                        registers[register] = val[0](convert(val[1]),
                                                     convert(val[2]))
                    check_parameter(register)
        waiting_for[p] = []
for instruction in instructions:
    args = instruction.strip().split(' ')
    if len(args) == 3:
        registers[args[2]] = (args[0],)
        waiting_for[args[0]].append(args[2])
        dependencies[args[2]].append(args[0])
        check_parameter(args[0])
    if len(args) == 4:
        registers[args[3]] = (operators[args[0]], args[1])
        waiting_for[args[1]].append(args[3])
        dependencies[args[3]].append(args[1])
        check_parameter(args[1])
    if len(args) == 5:
        registers[args[4]] = (operators[args[1]], args[0], args[2])
        waiting_for[args[0]].append(args[4])
        waiting_for[args[2]].append(args[4])
        dependencies[args[4]].append(args[0])
        dependencies[args[4]].append(args[2])
        check_parameter(args[0])
        check_parameter(args[2])
print('The value in wire a is {}'.format(registers['a']))
registers = {'b': registers['a']}
for instruction in instructions:
    args = instruction.strip().split(' ')
    if len(args) == 3:
        if args[2] == 'b':
            continue
        registers[args[2]] = (args[0],)
        waiting_for[args[0]].append(args[2])
        dependencies[args[2]].append(args[0])
        check_parameter(args[0])
    if len(args) == 4:
        registers[args[3]] = (operators[args[0]], args[1])
        waiting_for[args[1]].append(args[3])
        dependencies[args[3]].append(args[1])
        check_parameter(args[1])
    if len(args) == 5:
        registers[args[4]] = (operators[args[1]], args[0], args[2])
        waiting_for[args[0]].append(args[4])
        waiting_for[args[2]].append(args[4])
        dependencies[args[4]].append(args[0])
        dependencies[args[4]].append(args[2])
        check_parameter(args[0])
        check_parameter(args[2])
print('The new value in wire a is {}'.format(registers['a']))
