import json
lines = open('input.txt', 'r').read().strip().split('\n')
aunts = {}
for line in lines:
    args = line.strip().split(' ')
    nr = args[1].replace(':', '')
    aunts[nr] = {}
    for i in range(2, len(args), 2):
        aunts[nr][args[i].replace(':', '')] = int(args[i + 1].replace(',', ''))
sought = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
for aunt, props in aunts.items():
    for prop in sought:
        if prop in props and props[prop] != sought[prop]:
            break
    else:
        break
print('The number of the aunt that got the gift is {}.'.format(aunt))
for aunt, props in aunts.items():
    for prop in sought:
        if prop in props:
            if prop in ('cats', 'trees'):
                if props[prop] <= sought[prop]:
                    break
            elif prop in ('pomeranians', 'goldfish'):
                if props[prop] >= sought[prop]:
                    break
            elif props[prop] != sought[prop]:
                break
    else:
        break
print('The real number of the aunt that got the gift is {}.'.format(aunt))
