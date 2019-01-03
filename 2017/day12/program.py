from re import compile, match
from sys import argv

parser = compile(r'(?P<ID>\d+) <-> (?P<others>.+)$')
parsed = (match(parser, line).groupdict()
          for line in open(argv[1], 'r').read().strip().split('\n'))
connections = {line['ID']: tuple(other.strip()
                                 for other in line['others'].split(','))
               for line in parsed}


def check_connection(id, checked=None):
    checked = set() if checked is None else checked
    checked.add(id)
    for connection in connections[id]:
        if connection not in checked:
            check_connection(connection, checked)
    return checked


# Part 1

answer1 = len(check_connection('0'))
print('The group that contains program ID 0 contains {} programs'.format(
      answer1))


# Part 2

undetermined_programs = set(connections.keys())
groups = 0
while undetermined_programs:
    new_group = check_connection(undetermined_programs.pop())
    undetermined_programs -= new_group
    groups += 1
answer2 = groups
print('There are {} groups in total'.format(answer2))

