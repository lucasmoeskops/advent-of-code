from os import path
from sys import argv
from typing import IO
from lib.itertools import grouper


class ItemContainer(set):
    def is_safe(self):
        for item in self:
            if isinstance(item, Chip) \
                    and not filter(
                lambda item2: isinstance(item2, Generator)
                              and item2.powers(item), self):
                return False
        return True


class Chip:
    def __init__(self, compatibility: str):
        self.compatibility: str = compatibility


class Elevator(ItemContainer):
    def __init__(self, floor: int=0):
        super().__init__()


class Floor(ItemContainer):
    def __init__(self, level: int):
        super().__init__()
        self.level: int = level


class Generator:
    def __init__(self, compatibility: str):
        self.compatibility: str = compatibility

    def powers(self, chip: Chip):
        return chip.compatibility == self.compatibility


class Facility:
    def __init__(self):
        self.floors = []

    def construct(self, fp: IO):
        for level, line in enumerate(fp.read().strip().split('\n'), start=1):
            self.floors[level - 1] = floor = Floor(level)
            contents = \
                line.replace(',', '')\
                    .replace('.', '')\
                    .replace(' and ', ' ')\
                    .split(',')[4:]
            for item in grouper(contents, 3):
                parts = item.split(' ')
                if parts[0] == 'nothing':
                    break
                if parts[2] == 'generator':
                    floor.add(Generator(parts[1]))
                if parts[2] == 'microchip':
                    floor.add(Chip(parts[1].rsplit('-', 1)[0]))


def solve(fp=None):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    part1 = None
    part2 = None

    return (part1, part2)


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)
    simulate = '-m' in argv and (argv.remove('-m') or True)

    if len(argv) > 1:
        kwargs['fp'] = open(argv[1], 'r')

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


