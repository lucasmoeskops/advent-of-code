from collections import Counter
chars = open('input.txt', 'r').read().strip()
start = 0, 0
distribution = Counter({start: 1})
location = start
for char in chars:
    location = location[0] + {'<': -1, '>': 1}.get(char, 0),\
               location[1] + {'^': -1, 'v': 1}.get(char, 0)
    distribution[location] += 1
print('Santa visits {} distinct houses.'.format(len(distribution)))
distribution = Counter({start: 2})
locations = start, start
for i in range(0, len(chars), 2):
    locations = (locations[0][0] + {'<': -1, '>': 1}.get(chars[i], 0),\
                 locations[0][1] + {'^': -1, 'v': 1}.get(chars[i], 0)),\
                (locations[1][0] + {'<': -1, '>': 1}.get(chars[i + 1], 0),\
                 locations[1][1] + {'^': -1, 'v': 1}.get(chars[i + 1], 0))
    distribution[locations[0]] += 1
    distribution[locations[1]] += 1
print('Next year, Santa and Robo-Santa visit {} distinct houses'.format(
    len(distribution)))
