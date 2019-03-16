from collections import deque
from sys import argv
from termcolor import colored as term_colored
from typing import List, Tuple


class Maze:
    WALL = 0
    OPEN = 1

    def __getitem__(self, item: Tuple[int, int]):
        return Maze.WALL

    def show_map(
            self,
            width: int,
            height: int,
            colored: bool = False) -> Tuple[Tuple[str]]:
        mapping = {
            Maze.WALL: '#',
            Maze.OPEN: '.',
        }
        if colored:
            string: str = term_colored(mapping[Maze.WALL], 'blue')
            mapping[Maze.WALL] = string
        return tuple(tuple(mapping[self[(x, y)]] for x in range(width)) for y
                     in range(height))


class MagicMaze(Maze):
    def __init__(self, magic_number: int):
        self.magic_number: int = magic_number
        self.reference = {}

    def __getitem__(self, item: Tuple[int, int]):
        if item not in self.reference:
            x, y = item
            r = x*x + 3*x + 2*x*y + y + y*y
            r += self.magic_number
            r = sum(1 for character in bin(r) if character == '1') % 2
            self.reference[item] = Maze.WALL if r == 1 else Maze.OPEN
        return self.reference[item]


class AStarMazeSolver:
    def __init__(self, maze: Maze, starting_position: Tuple[int, int]):
        self.maze = maze
        self.starting_position: Tuple[int, int] = starting_position
        self.distances = {}
        self.explored: bool = False

    def distance_to(self, position: Tuple[int, int]) -> int:
        if position not in self.distances:
            self._solve(position)
        if position not in self.distances:
            raise ValueError('Couldn\'t solve')
        return self.distances[position]

    def get_path_to(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        if position not in self.distances:
            self._solve(position)
        if position not in self.distances:
            raise ValueError('Couldn\'t solve')
        rpath = [position]
        adjacent = (-1, 0), (1, 0), (0, -1), (0, 1)
        while self.distances[rpath[-1]] > 0:
            for option in adjacent:
                p = self._position_add(rpath[-1], option)
                if p not in self.distances:
                    continue
                if self.distances[p] < self.distances[rpath[-1]]:
                    rpath.append(p)
                    break
        return rpath[::-1]

    def show_solved_map(
            self,
            destination: Tuple[int, int],
            show_failures: bool = False,
            colored: bool = False):
        path = self.get_path_to(destination)
        map_source = self.distances if show_failures or self.explored else path
        width = max(map_source, key=lambda item: item[0])[0] + 2
        height = max(map_source, key=lambda item: item[1])[1] + 2
        base_map = self.maze.show_map(width, height, colored)
        maze_path = term_colored('O', 'green') if colored else 'O'
        maze_fail = term_colored('X', 'red') if colored else 'X'
        maze_explore = term_colored('+', 'yellow') if colored else '+'
        return tuple(tuple(maze_path if (x, y) in path else
                           (maze_explore if self.explored and (x, y) in
                            self.distances else (maze_fail if show_failures
                            and (x, y) in self.distances else base_map[y][x]))
                           for x in range(width)) for y in range(height))

    def _position_add(self, p1, p2):
        return p1[0] + p2[0], p1[1] + p2[1]

    def explore(self, steps: int):
        known = set()
        adjacent = (-1, 0), (1, 0), (0, -1), (0, 1)
        to_evaluate = deque([self.starting_position])
        self.distances[self.starting_position] = 0
        while to_evaluate:
            p = to_evaluate.popleft()
            if self.distances[p] < steps:
                for option in adjacent:
                    p2 = self._position_add(p, option)
                    if p2[0] < 0 or p2[1] < 0:
                        continue
                    if p2 in known:
                        continue
                    if self.maze[p2] == Maze.WALL:
                        continue
                    if p2 in to_evaluate:
                        self.distances[p2] = min(self.distances[p2],
                                                 self.distances[p] + 1)
                        continue
                    self.distances[p2] = self.distances[p] + 1
                    to_evaluate.append(p2)
            if self.distances[p] <= steps:
                known.add(p)
        self.explored = True
        return len(known)

    def _solve(self, position: Tuple[int, int]):
        def heuristic(p):
            return abs(position[0] - p[0]) + abs(position[1] - p[1])
        known = set()
        adjacent = (-1, 0), (1, 0), (0, -1), (0, 1)
        to_evaluate = deque([self.starting_position])
        self.distances[self.starting_position] = 0
        while to_evaluate:
            p = to_evaluate.popleft()
            if p == position:
                return
            h_p = heuristic(p)
            for option in adjacent:
                p2 = self._position_add(p, option)
                if p2[0] < 0 or p2[1] < 0:
                    continue
                if p2 in known:
                    continue
                if self.maze[p2] == Maze.WALL:
                    continue
                if p2 in to_evaluate:
                    self.distances[p2] = min(self.distances[p2],
                                             self.distances[p] + 1)
                    continue
                self.distances[p2] = self.distances[p] + 1
                if h_p > heuristic(p2):
                    to_evaluate.appendleft(p2)
                else:
                    to_evaluate.append(p2)
            known.add(p)


def solve(
        number: int = 1350,
        end_position: Tuple[int, int] = (31, 39),
        explore_steps: int = 50,
        simulate: bool = False,
        simulate_part2: bool = False,
        show_failures: bool = False,
        colored: bool = False):
    maze: Maze = MagicMaze(number)
    solver: AStarMazeSolver = AStarMazeSolver(maze, (1, 1))
    solver2: AStarMazeSolver = AStarMazeSolver(maze, (1, 1))

    if simulate:
        kwargs = {}
        if show_failures:
            kwargs['show_failures'] = True
        if colored:
            kwargs['colored'] = True
        if not simulate_part2:
            print(''.join((''.join(inner) + '\n' for inner in
                           solver.show_solved_map(end_position, **kwargs))))
        else:
            solver2.explore(explore_steps)
            print(''.join((''.join(inner) + '\n' for inner in
                           solver2.show_solved_map((1, 1), **kwargs))))

    part1: int = solver.distance_to(end_position)
    part2: int = solver2.explore(explore_steps)

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)
    simulate = '-m' in argv and (argv.remove('-m') or True)
    show_failures = '-f' in argv and (argv.remove('-f') or True)
    colored = '-c' in argv and (argv.remove('-c') or True)
    part2 = '-p2' in argv and (argv.remove('-p2') or True)

    if len(argv) > 1:
        kwargs['number'] = int(argv[1])

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


