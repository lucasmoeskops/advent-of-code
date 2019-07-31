from math import ceil
from sys import argv
from typing import NamedTuple, List


class Spell(NamedTuple):
    name: str
    costs: int
    duration: int


class Fighter(NamedTuple):
    hp: int
    dmg: int = 0
    armor: int = 0
    mana: int = 0


magic_missile = Spell('Magic Missile', 53, 0)
drain = Spell('Drain', 73, 0)
shield = Spell('Shield', 113, 6)
poison = Spell('Poison', 173, 6)
recharge = Spell('Recharge', 229, 5)

spells = magic_missile, drain, shield, poison, recharge

lines = open('input.txt'
             if len(argv) < 2 else argv[1], 'r').read().strip().split('\n')
boss = Fighter(*(int(line.split(':')[1]) for line in lines))

player = Fighter(50, mana=500)


def fight(player: Fighter, opponent: Fighter, recharge_times: int,
          shield_safety: int, hard_mode: bool = False):
    def apply_effects():
        nonlocal mana, opponent_hp_left

        if spell_timeout[poison]:
            opponent_hp_left -= 3
            spell_timeout[poison] -= 1

        if spell_timeout[shield]:
            spell_timeout[shield] -= 1

        if spell_timeout[recharge]:
            mana += 101
            spell_timeout[recharge] -= 1

    mana = player.mana
    mana_spent = 0
    spell_timeout = {spell: 0 for spell in spells}
    player_hp_left = player.hp
    opponent_hp_left = opponent.hp
    turn = 1
    plan = []
    spell_order = poison, shield, recharge, drain, magic_missile

    while True:
        if hard_mode:
            player_hp_left -= 1

            if player_hp_left < 1:
                # Nooo
                return []

        apply_effects()

        if opponent_hp_left < 1:
            # We won!
            return plan

        if hard_mode:
            survive_turns = min(spell_timeout[shield] // 2, player_hp_left - 1)
        else:
            survive_turns = min(spell_timeout[shield] // 2, player_hp_left)

        if spell_timeout[shield] < player_hp_left:
            turn_damage = opponent.dmg + (1 if hard_mode else 0)
            survive_turns += ceil((player_hp_left - spell_timeout[shield])
                                  / turn_damage)

        # Can we simply kill the opponent with magic missile?
        can_kill = opponent_hp_left <= 4 + (3 if spell_timeout[poison] else 0)

        should_use = {
            # Use drain at the last possible moment, to stay alive, unless we
            # can kill the opponent instead
            drain: player_hp_left == 1 and not can_kill,

            # Shield at last moment. Assuming the opponent does 1 damage with
            # shield. Unless we can kill the opponent instead
            shield: (not spell_timeout[shield]
                     and player_hp_left < (opponent.dmg + (1 if hard_mode else 0)) * shield_safety
                     and not can_kill),

            # Use recharge as experiment, for as long as recharge_times
            # available.
            recharge: (not spell_timeout[recharge] and recharge_times
                       and not can_kill),

            # Poison does more damage than magic missile, unless the opponent
            # is nearly dead, up to three magic missiles are cheaper then
            # poison, if we survive for that long
            poison: (not spell_timeout[poison]
                     and opponent_hp_left > 4 * min(4, survive_turns)),

            # The trustworthy remaining option, if there is mana
            magic_missile: True
        }

        # Cast the first matching spell
        for spell in spell_order:
            if should_use[spell] and mana > spell.costs:
                print(spell.name, player_hp_left, opponent_hp_left)
                if spell == recharge:
                    recharge_times -= 1

                if spell == magic_missile:
                    opponent_hp_left -= 4

                if spell == drain:
                    player_hp_left += 2
                    opponent_hp_left -= 2

                if spell == shield:
                    shield_safety = 1

                plan.append(spell)
                spell_timeout[spell] = spell.duration
                mana -= spell.costs
                mana_spent += spell.costs
                break
        else:
            # No spell could be cast, we are dead
            return []

        turn += 1

        apply_effects()

        if opponent_hp_left < 1:
            # We won!
            print(mana, mana_spent)
            return plan

        # Assume shield reduces incoming damage to 1
        player_hp_left -= 1 if spell_timeout[shield] else opponent.dmg

        if player_hp_left < 1:
            # We died :-(
            return []


def calc_best_result(result, other_result):
    costs = sum(spell.costs for spell in result)

    if not other_result:
        return result, costs

    other_costs = sum(spell.costs for spell in other_result)

    if costs < other_costs:
        return result, costs

    return other_result, other_costs


recharge_times = 0
best_result = None
best_costs = -1

while not best_result and recharge_times < boss.hp:
    recharge_times += 1

    for safety in range(1, 4):
        result = fight(player, boss, recharge_times, safety)

        if result:
            best_result, best_costs = calc_best_result(result, best_result)


print(', '.join(spell.name for spell in best_result))

print(f'The least amount of mana that can be spent to kill the boss is'
      f' {best_costs}')


recharge_times = 0
best_result = None
best_costs = -1

while not best_result and recharge_times < boss.hp:
    for safety in range(1, 7):
        result = fight(player, boss, recharge_times, safety, True)

        if result:
            best_result, best_costs = calc_best_result(result, best_result)

    recharge_times += 1


print(', '.join(spell.name for spell in best_result))

print(f'The least amount of mana that can be spent to kill the boss on'
      f' hard mode is {best_costs}')
