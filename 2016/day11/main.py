from collections import deque, defaultdict
from functools import partial, reduce
from itertools import combinations, chain, count
from operator import methodcaller
from os import path
from string import ascii_uppercase
from sys import argv
from time import sleep
from typing import IO, List
from lib.itertools import grouper
from lib.os import clear_terminal

LOAD_ELEVATOR = 1
LOAD_FLOOR = 2
MOVE_ELEVATOR_UP = 3
MOVE_ELEVATOR_DOWN = 4


def get_unique_letterer():
    def abbreviate(name):
        nonlocal options
        for letter in name.upper():
            if letter in options:
                options = [option for option in options if option != letter]
                return letter
    options = ascii_uppercase
    return abbreviate


class ItemContainer(set):
    def is_safe(self):
        def is_generator(item):
            return isinstance(item, Generator)
        for item in self:
            if isinstance(item, Chip):
                has_generator = any(filter(is_generator, self))
                has_protection = any(filter(methodcaller('powers', item), filter(is_generator, self)))
                if has_generator and not has_protection:
                    return False
        return True


class RadiationError(Exception):
    pass


class Chip:
    def __init__(self, compatibility: str, abbreviation: str):
        self.compatibility: str = compatibility
        self.abbreviation: str = abbreviation

    def clone(self):
        return Chip(self.compatibility)

    def __repr__(self):
        return self.compatibility

    def __str__(self):
        return '{}M'.format(self.abbreviation)


class Elevator(ItemContainer):
    LOADING = 0
    UNLOADING = 1
    FILLED = 2

    def __init__(self, level: int = 0, phase: int = LOADING):
        super().__init__()
        self.level = level
        self.phase = phase

    def clone(self):
        clone = Elevator(self.level, self.phase)
        clone.update(self)
        return clone


class Floor(ItemContainer):
    def __init__(self):
        super().__init__()

    def clone(self):
        clone = Floor()
        clone.update(self)
        return clone


class Generator:
    def __init__(self, compatibility: str, abbreviation: str):
        self.compatibility: str = compatibility
        self.abbreviation: str = abbreviation

    def powers(self, chip: Chip):
        return chip.compatibility == self.compatibility

    def clone(self):
        return Generator(self.compatibility)

    def __repr__(self):
        return self.compatibility

    def __str__(self):
        return '{}G'.format(self.abbreviation)


class Facility:
    def __init__(self):
        self.floors = []
        self.elevator = Elevator(0)

    @property
    def state(self):
        chips = count(1)
        generators = count(1)
        state = []
        for index, floor in enumerate(self.floors):
            if self.elevator.level == index:
                containers = floor, self.elevator
            else:
                containers = floor,
            items: List[int] = []
            for item in chain(*containers):
                if isinstance(item, Chip):
                    items.append(next(chips))
                else:
                    items.append(- next(generators))
            state.append(tuple(sorted(items)))
        state.append((self.elevator.level, self.elevator.phase))
        return tuple(state)

    def construct(self, fp: IO):
        abb_namer = get_unique_letterer()
        abb_names = {}
        for level, line in enumerate(fp.read().strip().split('\n'), start=1):
            floor = Floor()
            self.floors.append(floor)
            contents = \
                line.replace(',', '')\
                    .replace('.', '')\
                    .replace(' and ', ' ')\
                    .split(' ')[4:]
            for parts in grouper(contents, 3):
                if parts[0] == 'nothing':
                    break
                if parts[2] == 'generator':
                    name = parts[1]
                    abb_names[name] = abb_names.get(name, abb_namer(name))
                    floor.add(Generator(name, abb_names[name]))
                if parts[2] == 'microchip':
                    name = parts[1].rsplit('-', 1)[0]
                    abb_names[name] = abb_names.get(name, abb_namer(name))
                    floor.add(Chip(name, abb_names[name]))

    def clone(self):
        clone = Facility()
        clone.elevator = self.elevator.clone()
        clone.floors = [floor.clone() for floor in self.floors]
        return clone


class Situation:
    def __init__(self, facility: Facility):
        self.facility = facility
        self.steps = 0
        self.actions = [(None, facility.clone())]

    @property
    def current_floor(self):
        return self.facility.floors[self.current_level]

    @property
    def current_level(self):
        return self.facility.elevator.level

    def available_actions(self):
        actions = []
        if len(self.facility.elevator):
            if self.facility.elevator.level > 0:
                actions.append((MOVE_ELEVATOR_DOWN,))
            if self.facility.elevator.level + 1 < len(self.facility.floors):
                actions.append((MOVE_ELEVATOR_UP,))
        if self.facility.elevator.phase == Elevator.LOADING\
                and len(self.current_floor)\
                and len(self.facility.elevator) < 2:
            for item1, item2 in combinations(self.current_floor ^ {None}, 2):
                if ItemContainer(self.current_floor - {item1, item2}).is_safe():
                    actions.append((LOAD_ELEVATOR, [item1, item2]))
        if self.facility.elevator.phase == Elevator.UNLOADING\
                and len(self.facility.elevator):
            actions.append((LOAD_FLOOR, self.facility.elevator))
        return actions

    def perform_action(self, action: tuple):
        action_type, params = action[0], action[1:]
        if action_type in (MOVE_ELEVATOR_DOWN, MOVE_ELEVATOR_UP):
            delta = 1 if action_type == MOVE_ELEVATOR_UP else -1
            if not self.current_floor.is_safe():
                raise RadiationError
            self.facility.elevator.level += delta
            if not ItemContainer(self.current_floor ^ self.facility.elevator).is_safe():
                raise RadiationError
            self.facility.elevator.phase = Elevator.UNLOADING
            self.steps += 1
        elif action_type == LOAD_ELEVATOR:
            for param in params[0]:
                self.transfer(param)
            self.facility.elevator.phase = Elevator.FILLED
        elif action_type == LOAD_FLOOR:
            for param in params[0]:
                self.transfer(param)
            self.facility.elevator.phase = Elevator.LOADING
        self.actions.append((action, self.facility))

    def transfer(self, item):
        from_ = None
        to_ = None
        if item in self.facility.elevator:
            from_ = self.facility.elevator
            to_ = self.current_floor
        elif item in self.current_floor:
            from_ = self.current_floor
            to_ = self.facility.elevator
        if from_:
            from_.remove(item)
            to_.add(item)
            return True
        return False

    def is_desired_situation(self):
        return not any(map(len, self.facility.floors[:-1]))\
               and not len(self.facility.elevator)

    def clone(self):
        facility_clone = self.facility.clone()
        clone = Situation(facility_clone)
        clone.steps = self.steps
        clone.actions = self.actions[:]
        return clone


class Simulator:
    def __init__(self, situation: Situation):
        self.situation: Situation = situation
        self.items: List[ItemContainer] = sorted(
            situation.facility.elevator
            ^ reduce(set.union, situation.facility.floors), key=str)

    def start(self):
        first = True
        for action in self.situation.actions:
            if action[0] is None \
                    or action[0][0] in (MOVE_ELEVATOR_DOWN, MOVE_ELEVATOR_UP):
                self._show_frame(action[1])
                sleep(5 if first else 2)
                first = False

    def _show_frame(self, facility: Facility):
        clear_terminal()
        print('')
        for index, floor in reversed(tuple(enumerate(facility.floors, 1))):
            print('  ', end='')
            has_elevator: bool = index == facility.elevator.level + 1
            print('F' + str(index), end=' ')
            if has_elevator:
                print('E', end='  ')
            else:
                print('.', end='  ')
            for item in self.items:
                if item in floor \
                        or has_elevator and item in facility.elevator:
                    print(str(item), end=' ')
                else:
                    print('. ', end=' ')
            print('')


def solver(situation: Situation, simulate: bool = False, simulate_expect: int=0):
    def prepare_action(situation, action):
        return situation.clone(), action
    seen_states = set()
    seen_states.add(situation.facility.state)
    pending_situations = defaultdict(deque)
    prepare_action_partial = partial(prepare_action, situation)
    pending_situations[0] = \
        deque(map(prepare_action_partial, situation.available_actions()))
    step = 0
    while pending_situations[step]:
        situation, action = pending_situations[step].popleft()
        try:
            situation.perform_action(action)
        except RadiationError:
            pass
        else:
            state = situation.facility.state
            if state not in seen_states\
                    or action[0] in (LOAD_FLOOR, LOAD_ELEVATOR):
                seen_states.add(state)
                if situation.is_desired_situation():
                    return situation
                prepare_action_partial = partial(prepare_action, situation)
                new_actions = \
                    deque(map(prepare_action_partial,
                              situation.available_actions()))
                pending_situations[situation.steps].extend(new_actions)
        if not pending_situations[step]:
            step += 1
            if simulate and simulate_expect > 0:
                print('{}%'.format(step * 100 // simulate_expect))
    return None


def solve(fp=None, simulate=False):
    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    facility = Facility()
    facility.construct(fp)

    facility2 = facility.clone()
    facility2.floors[0].add(Chip('elerium', 'E'))
    facility2.floors[0].add(Chip('dilithium', 'D'))
    facility2.floors[0].add(Generator('elerium', 'E'))
    facility2.floors[0].add(Generator('dilithium', 'D'))

    situation = Situation(facility)
    situation2 = Situation(facility2)

    solution = solver(situation, simulate, 31)
    if simulate:
        Simulator(solution).start()
        input('Press [Enter] key to continue')
    solution2 = solver(situation2, simulate, 55)
    if simulate:
        Simulator(solution2).start()
        input('Press [Enter] key to continue')

    part1 = solution.steps if solution else None
    part2 = solution2.steps if solution else None

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)
    kwargs['simulate'] = '-m' in argv and (argv.remove('-m') or True)

    if len(argv) > 1:
        kwargs['fp'] = open(argv[1], 'r')

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


