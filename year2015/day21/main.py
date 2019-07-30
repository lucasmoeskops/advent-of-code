from math import ceil
from operator import attrgetter
from sys import argv
from typing import NamedTuple


class Fighter(NamedTuple):
    hp: int
    dmg: int
    armor: int


class Item(NamedTuple):
    name: str
    cost: int
    dmg: int
    armor: int


def fight(fighter1, fighter2):
    turns1 = ceil(fighter2.hp / max(1, fighter1.dmg - fighter2.armor))
    turns2 = ceil(fighter1.hp / max(1, fighter2.dmg - fighter1.armor))
    return turns1 - 1 < turns2  # player 1 always begins


weapons = (
    Item('Dagger', 8, 4, 0),
    Item('Shortsword', 10, 5, 0)
    ,
    Item('Warhammer', 25, 6, 0),
    Item('Longsword', 40, 7, 0),
    Item('Greataxe', 74, 8, 0),
)
armors = (
    Item('Leather', 13, 0, 1),
    Item('Chainmail', 31, 0, 2),
    Item('Splintmail', 53, 0, 3),
    Item('Bandedmail', 75, 0, 4),
    Item('Platemail', 102, 0, 5),
)
rings = (
    Item('Damage +1', 25, 1, 0),
    Item('Damage +2', 50, 2, 0),
    Item('Damage +3', 100, 3, 0),
    Item('Armor +1', 20, 0, 1),
    Item('Armor +2', 40, 0, 2),
    Item('Armor +3', 80, 0, 3),
)


lines = open('input.txt'
             if len(argv) < 2 else argv[1], 'r').read().strip().split('\n')
boss = Fighter(*(int(line.split(':')[1]) for line in lines))

outfits = []
for weapon in weapons:
    for armor in ((None,) + armors):
        for ring1 in ((None,) + rings):
            for ring2 in ((None,) + rings):
                if ring1 == ring2:
                    continue
                combo = (weapon, armor, ring1, ring2)
                combo = tuple(item for item in combo if item)
                name = ' '.join(f'[{item.name}]' for item in combo)
                cost = sum(item.cost for item in combo)
                dmg = sum(item.dmg for item in combo)
                armor_stat = sum(item.armor for item in combo)
                outfits.append(Item(name, cost, dmg, armor_stat))
outfits = sorted(outfits, key=attrgetter('cost'))

for outfit in outfits:
    outfitted_fighter = Fighter(100, outfit.dmg, outfit.armor)
    if fight(outfitted_fighter, boss):
        break
print(f'Least cost is {outfit.cost} for outfit {outfit.name}')

for outfit in reversed(outfits):
    outfitted_fighter = Fighter(100, outfit.dmg, outfit.armor)
    if not fight(outfitted_fighter, boss):
        break
print(f'Least efficient outfit is {outfit.name} with cost {outfit.cost}.')
