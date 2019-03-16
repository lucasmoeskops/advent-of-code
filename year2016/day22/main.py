import re
from operator import attrgetter
from os import path
from sys import argv


class Node:
    def __init__(self, space_total, space_available):
        self.space_total = space_total
        self.space_available = space_available

    @property
    def space_used(self):
        return self.space_total - self.space_available

    def __repr__(self):
        return '({}, {}, {})'.format(self.space_total, self.space_used,
                                     self.space_available)


class NodeGrid:
    def __init__(self):
        self.nodes = {}
        self.width = 0
        self.height = 0

    def add_node(self, x, y, node):
        self.nodes[complex(x, y)] = node
        self.width = max(self.width, x + 1)
        self.height = max(self.height, y + 1)

    def viable_pairs(self):
        nodes_a = sorted(self.nodes.values(), key=attrgetter('space_used'),
                         reverse=True)
        nodes_b = sorted(self.nodes.values(), key=attrgetter(
            'space_available'))
        viable = 0
        skip = 0
        for a in nodes_a:
            for i, b in enumerate(nodes_b[skip:], start=skip):
                if a.space_used <= b.space_available:
                    skip = i
                    viable += len(nodes_b) - skip
                    if a.space_used <= a.space_available:
                        viable -= 1
                    break

        return viable

    def move_data(self, xa, ya, xb, yb):
        node_a = self.nodes[complex(xa, ya)]
        node_b = self.nodes[complex(xb, yb)]
        adjacent = abs(xa - xb) + abs(ya - yb) == 1
        if node_a.space_used < node_b.space_available and adjacent:
            node_b.space_available -= node_a.space_used
            node_a.space_available = node_a.space_total
        else:
            raise RuntimeError('Not a valid move: ({}, {}) -> ({}, '
                               '{})'.format(xa, ya, xb, yb))

    def print_map(self):
        adjacent = 0+1j, 0-1j, 1+0j, -1+0j
        space_required = self.nodes[complex(self.width - 1, 0)].space_used
        for y in range(self.height):
            for x in range(self.width):
                node = self.nodes.get(complex(x, y))
                if node.space_used >= 90:#space_required:
                    print('#', end='')
                elif node.space_available >= space_required:
                    print('_', end='')
                else:
                    print('.', end='')
                continue
                for a in adjacent:
                    a_node = self.nodes.get(complex(x, y) + a)
                    if a_node and node.space_available >= a_node.space_used:
                        break
                else:
                    print('.', end='')
                    continue
                print('_', end='')
            print('')


def parse_grid(data):
    node_grid = NodeGrid()
    for node in data[2:]:
        params = tuple(map(int, re.findall(r'\d+', node)))
        node_grid.add_node(params[0], params[1], Node(params[2], params[4]))
    return node_grid


def get_data_at_origin(x, y, node_grid):
    """ move data from (x, y) to (0, 0); return steps required """
    good_node = complex(24, 26)
    for i in range(27):
        node_grid.move_data(24, 25 - i, 24, 26 - i)

    node_grid.print_map()
    return
    target_node = node_grid.nodes[complex(x, y)]
    next_node = node_grid.nodes.get(complex(x - 1, y))
    down_node = node_grid.nodes.get(complex(x, y - 1))
    up_node = node_grid.nodes.get(complex(x, y + 1))
    if x > 0 and target_node.space_used <= next_node.space_available:
        print('left!')
        node_grid.move_data(x, y, x - 1, y)
        return 1 + get_data_at_origin(x - 1, y, node_grid)
    elif y > 0 and target_node.space_used <= down_node.space_available:
        print('down!')
        node_grid.move_data(x, y, x, y - 1)
        return 1 + get_data_at_origin(x, y - 1, node_grid)
    elif y + 1 < node_grid.height \
            and target_node.space_used <= up_node.space_available:
        print('up!')
        node_grid.move_data(x, y, x, y + 1)
        return 1 + get_data_at_origin(x, y + 1, node_grid)
    else:
        node_grid.print_map()


def solve(fp=None, visualize=False):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    node_data = fp.read().strip().split('\n')
    node_grid = parse_grid(node_data)

    if visualize:
        node_grid.print_map()

    part1 = node_grid.viable_pairs()
    part2 = get_data_at_origin(node_grid.width - 1, 0, node_grid)

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)
    kwargs['visualize'] = '-v' in argv and (argv.remove('-v') or True)

    if len(argv) > 1:
        kwargs['fp'] = open(argv[1])

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


