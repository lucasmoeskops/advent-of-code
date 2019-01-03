from itertools import cycle
from sys import argv

if argv[1][-4:] == '.txt':
    route = open(argv[1], 'r').read().strip().split(',')
else:
    route = argv[1].split(',')

options = 'nw', 'n', 'ne', 'se', 's', 'sw'


def optimize(route):
    for option in options:
        counter_option = (options + options)[options.index(option) + 3]
        rewrite_option = (options + options)[options.index(option) + 2]
        rewrite_to = (options + options)[options.index(option) + 1]
        while option in route and counter_option in route:
            route.remove(option)
            route.remove(counter_option)
        while option in route and rewrite_option in route:
            route.remove(option)
            route.remove(rewrite_option)
            route.append(rewrite_to)

# Part 1

route1 = route[:]
optimize(route1)
answer1 = len(route1)
print('Destination is reachable in {} steps'.format(answer1))


# Part 2
farthest_away = 0
route2 = []
for i in range(len(route)):
    route2.append(route[i])
    optimize(route2)
    farthest_away = max(farthest_away, len(route2))
answer2 = farthest_away
print('Farthest away from starting points is {} steps'.format(answer2))

