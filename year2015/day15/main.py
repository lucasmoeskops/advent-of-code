from collections import Counter
from functools import reduce
from itertools import permutations
from operator import itemgetter
lines = open('input.txt', 'r').read().strip().split('\n')
ingredients = {}
recipe = Counter()
def calc_score(recipe):
    return reduce(int.__mul__, (max(0, sum(v * ingredients[i][p]
                                           for i, v in recipe.items()))
                                for p in range(4)))
def calc_raw_score(recipe):
    return reduce(int.__mul__, (sum(v * ingredients[i][p]
                                    for i, v in recipe.items())
                                for p in range(4)))
def calc_calories(recipe):
    return sum(v * ingredients[i][4] for i, v in recipe.items())
for line in lines:
    args = line.replace(',', '').strip().split(' ')
    ingredients[args[0].replace(':', '')] = (int(args[2]),
                                             int(args[4]),
                                             int(args[6]),
                                             int(args[8]),
                                             int(args[10]))
for ingredient in ingredients:
    recipe[ingredient] = 100 // len(ingredients)
a_change = True
while a_change:
    a_change = False
    for ing1, ing2 in permutations(ingredients.keys(), 2):
        while True:
            recipe2 = recipe.copy()
            recipe2[ing1] -= 1
            recipe2[ing2] += 1
            if calc_score(recipe2) <= calc_score(recipe):
                break
            recipe = recipe2
            a_change = True
print('The optimal recipe has score {} ({}).'.format(calc_score(recipe),
                                                     dict(recipe)))
while calc_calories(recipe) > 500:
    for ing1, ing2 in permutations(ingredients.keys(), 2):
        if ingredients[ing1][4] >= ingredients[ing2][4]:
            continue
        while calc_calories(recipe) > 500:
            recipe[ing1] += 1
            recipe[ing2] -= 1
            if calc_score(recipe) <= 0:
                # loose it up a little
                recipe[ing1] -= 10
                recipe[ing2] += 10
                break
a_change = True
while a_change:
    a_change = False
    for ing1, ing2 in permutations(ingredients.keys(), 2):
        if ingredients[ing1][4] != ingredients[ing2][4]:
            continue
        while True:
            recipe2 = recipe.copy()
            recipe2[ing1] -= 1
            recipe2[ing2] += 1
            if calc_score(recipe2) <= calc_score(recipe):
                break
            recipe = recipe2
            a_change = True
if calc_calories(recipe) == 500 and sum(recipe.values()) == 100:
    print('The optimal 500 calories recipe has score {} ({}).'.format(
        calc_score(recipe), dict(recipe)))
else:
    print('Failed to find answer for 2.')
