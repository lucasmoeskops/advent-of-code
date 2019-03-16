from functools import reduce
from os import path
from itertools import chain, permutations
from string import digits
from sys import argv
from termcolor import colored as term_colored
from typing import List, Tuple

from year2016.day13.main import Maze, AStarMazeSolver


class DefinedMaze(Maze):
    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def __getitem__(self, item: Tuple[int, int]):
        return self.data[item[1] * self.width + item[0]]

    def show_map(
            self,
            width: int = None,
            height: int = None,
            colored: bool = False):
        width = self.width if width is None else width
        height = self.height if height is None else height
        return super().show_map(width, height, colored)


def parse_maze(data_string):
    lines = data_string.split('\n')
    width = len(lines[0])
    height = len(lines)
    mapping = {
        '#': Maze.WALL,
        '.': Maze.OPEN,
    }
    for i in range(10):
        mapping[str(i)] = Maze.OPEN
    return DefinedMaze(width, height, [mapping[p] for p in
                                       chain.from_iterable(lines)])


def find_points_of_interest(data_string):
    lines = data_string.split('\n')
    width = len(lines[0])
    height = len(lines)
    points = {}
    for y in range(height):
        for x in range(width):
            if lines[y][x] in digits:
                points[lines[y][x]] = x, y
    return points


def find_routes(start_point, distance_dict, return_to_start=False):
    options = set(distance_dict.keys()) - {start_point}
    distances = {}
    for permutation in permutations(options, len(options)):
        if return_to_start:
            permutation = permutation + (start_point,)
        distances[permutation] = reduce(
            lambda acc, point: (point, acc[1] + distance_dict[acc[0]][
                point]),
            permutation,
            (start_point, 0))[1]
    return distances


def solve(
        fp=None,
        end_position: Tuple[int, int] = (31, 39),
        explore_steps: int = 50,
        simulate: bool = False,
        simulate_part2: bool = False,
        show_failures: bool = False,
        colored: bool = False):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')
    data_string = fp.read().strip()
    maze: Maze = parse_maze(data_string)
    points = find_points_of_interest(data_string)
    distances = {}
    for start in points.values():
        sub_distances = {}
        for point in points.values():
            if point in distances:
                sub_distances[point] = distances[point][start]
            else:
                sub_distances[point] = AStarMazeSolver(maze, start).distance_to(
                    point)
        distances[start] = sub_distances

    if simulate:
        kwargs = {}
        if show_failures:
            kwargs['show_failures'] = True
        if colored:
            kwargs['colored'] = True
        # if not simulate_part2:
        #     print(''.join((''.join(inner) + '\n' for inner in
        #                    solver.show_solved_map(end_position, **kwargs))))
        # else:
        #     solver2.explore(explore_steps)
        #     print(''.join((''.join(inner) + '\n' for inner in
        #                    solver2.show_solved_map((1, 1), **kwargs))))

    route = find_routes(points['0'], distances)

    part1: int = min(find_routes(points['0'], distances).values())
    part2: int = min(find_routes(points['0'], distances, True).values())

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)
    simulate = '-m' in argv and (argv.remove('-m') or True)
    show_failures = '-f' in argv and (argv.remove('-f') or True)
    colored = '-c' in argv and (argv.remove('-c') or True)
    part2 = '-p2' in argv and (argv.remove('-p2') or True)

    if len(argv) > 1:
        kwargs['fp'] = open(argv[1], 'r')

    if len(argv) > 3:
        kwargs['end_position'] = int(argv[2]), int(argv[3])

    if len(argv) > 4:
        kwargs['explore_steps'] = int(argv[4])

    kwargs['simulate'] = simulate
    kwargs['show_failures'] = show_failures
    kwargs['colored'] = colored
    kwargs['simulate_part2'] = part2

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


