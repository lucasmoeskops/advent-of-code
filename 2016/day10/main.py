import re
from functools import reduce
from operator import attrgetter, itemgetter
from os import path
from sys import argv
from typing import List, Dict, Set, Tuple, Type, Optional, Callable, Union

ChipReceiverAddress = Tuple[Type['ChipReceiver'], int]
Instruction = Type[Union['AssignmentInstruction', 'DeliveryInstruction']]
simulate = False


class ChipReceiver:
    def __init__(self):
        self.chips: List[MicroChip] = []

    def give_chip(self, chip: 'MicroChip'):
        self.chips.append(chip)

    def __str__(self):
        return ';'.join(map(str, self.chips))


class EventEmitter:
    def __init__(self):
        self.listeners: List[Tuple[str, Callable[[Dict], None]]] = []

    def on(self, event_type: str, callback: Callable):
        self.listeners.append((event_type, callback))

    def emit(self, event_type, emission: Dict):
        for listener in self.listeners:
            if listener[0] == event_type:
                listener[1](emission)


class AssignmentInstruction:
    def __init__(self, bot: int, value: int):
        self.bot: int = bot
        self.value: int = value


class Bin(ChipReceiver):
    pass


class Bot(ChipReceiver, EventEmitter):
    def __init__(self):
        ChipReceiver.__init__(self)
        EventEmitter.__init__(self)
        self.lowest_target: Optional[ChipReceiver] = None
        self.highest_target: Optional[ChipReceiver] = None
        self.delivery_known = False

    def set_delivery(self,
                     lowest_target: ChipReceiver,
                     highest_target: ChipReceiver):
        self.lowest_target = lowest_target
        self.highest_target = highest_target
        self.delivery_known = True
        self._proceed()

    def give_chip(self, chip: 'MicroChip'):
        super().give_chip(chip)
        self._proceed()

    def _proceed(self):
        if len(self.chips) == 2 and self.delivery_known:
            chips = (self.chips.pop(), self.chips.pop())
            self.emit('delivery', {'chips': chips})
            self.lowest_target.give_chip(min(chips))
            self.highest_target.give_chip(max(chips))


def assign(value: str, bot: str):
    return AssignmentInstruction(int(bot), int(value))


def delivery(deliverer: str,
             low_receiver_type: str,
             low_receiver_id: str,
             high_receiver_type: str,
             high_receiver_id: str):
    type_map = {'bot': Bot, 'output': Bin}
    low_receiver: ChipReceiverAddress = (type_map[low_receiver_type],
                                         int(low_receiver_id))
    high_receiver: ChipReceiverAddress = (type_map[high_receiver_type],
                                          int(high_receiver_id))
    return DeliveryInstruction(int(deliverer), low_receiver, high_receiver)


class Computer:
    capabilities: Dict[Callable, str] = {
        assign: r'value (?P<value>\d+) goes to bot (?P<bot>\d+)',
        delivery: r'bot (?P<deliverer>\d+) gives low to '
                  r'(?P<low_receiver_type>(bot|output)) '
                  r'(?P<low_receiver_id>\d+) and high to '
                  r'(?P<high_receiver_type>(bot|output)) '
                  r'(?P<high_receiver_id>\d+)',
    }

    def __init__(self, instruction_receivers: Dict[Instruction, Callable]):
        self.instruction_receivers: Dict[Instruction, Callable] = \
            instruction_receivers

    def parse_instructions(self, instructions: List[str]):
        for instruction in instructions:
            for capability, pattern in self.capabilities.items():
                match = re.match(pattern, instruction)
                if match:
                    instruction = capability(**match.groupdict())
                    self.instruction_receivers[instruction.__class__](instruction)
                    break


class DeliveryInstruction:
    def __init__(self,
                 deliverer: int,
                 low_target: ChipReceiverAddress,
                 high_target: ChipReceiverAddress):
        self.deliverer: int = deliverer
        self.low_target: ChipReceiverAddress = low_target
        self.high_target: ChipReceiverAddress = high_target


class Factory(EventEmitter):
    def __init__(self):
        super().__init__()
        self.bots: Dict[int, Bot] = {}
        self.bins: Dict[int, Bin] = {}
        self.chips: Set[MicroChip] = set()
        self.computer: Computer = Computer({
            AssignmentInstruction: self.assign_chip,
            DeliveryInstruction: self.assign_delivery,
        })

    def assign_chip(self, instruction: 'AssignmentInstruction'):
        self._ensure_bot(instruction.bot)
        self._ensure_chip(instruction.value)
        chip: MicroChip = next(
            filter(lambda a_chip: a_chip.value == instruction.value, self.chips))
        if simulate:
            print('Bot {} receives chip value-{}'.format(instruction.bot, chip.value))
        self.bots[instruction.bot].give_chip(chip)
        self.chips.remove(chip)  # the bot has it

    def assign_delivery(self, instruction: 'DeliveryInstruction'):
        self._ensure_bot(instruction.deliverer)
        targets: List[Optional[ChipReceiver], Optional[ChipReceiver]] = \
            [None, None]
        for index, target in enumerate((instruction.low_target,
                                       instruction.high_target)):
            if target[0] == Bin:
                self._ensure_bin(target[1])
                targets[index] = self.bins[target[1]]
            elif target[0] == Bot:
                self._ensure_bot(target[1])
                targets[index] = self.bots[target[1]]
            else:
                raise ValueError('Unknown target {}'.format(target[0]))
        self.bots[instruction.deliverer].set_delivery(*targets)

    def _ensure_bin(self, bin: int):
        if bin not in self.bins:
            self.bins[bin] = Bin()

    def _ensure_bot(self, bot_id: int):
        def on_delivery(emission: Dict):
            if simulate:
                print(
                    'Bot {} delivers {} and {}'.format(
                        bot_id,
                        emission['chips'][0].value,
                        emission['chips'][1].value))
            self.emit('delivery', {
                'bot_id': bot_id,
                'chips': emission['chips'],
            })

        if bot_id not in self.bots:
            self.bots[bot_id] = bot = Bot()
            bot.on('delivery', on_delivery)

    def _ensure_chip(self, value: int):
        if value not in self.chips:
            self.chips.add(MicroChip(value))


class MicroChip:
    def __init__(self, value: int):
        self.value: int = value

    def __gt__(self, other: 'MicroChip'):
        return self.value > other.value

    def __lt__(self, other: 'MicroChip'):
        return self.value < other.value

    def __str__(self):
        return str(self.value)


def solve(fp=None):
    def check_delivery(delivery: Dict):
        nonlocal part_1_answer

        if tuple(map(attrgetter('value'), delivery['chips'])) == (17, 61):
            part_1_answer = delivery['bot_id']

    if fp is None:
        dir_path = path.dirname(path.realpath(__file__))
        file_path = path.join(dir_path, 'input.txt')
        fp = open(file_path, 'r')

    part_1_answer: Optional[int] = None
    instructions = fp.read().strip().split('\n')
    factory = Factory()
    factory.on('delivery', check_delivery)
    computer = factory.computer
    computer.parse_instructions(instructions)

    part1 = part_1_answer
    part2 = reduce(int.__mul__,
                   (bin.chips[0].value
                    for bin in itemgetter(0, 1, 2)(factory.bins)))

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


