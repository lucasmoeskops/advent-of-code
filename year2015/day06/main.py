instructions = open('input.txt', 'r').read().strip().split('\n')
lights = [False] * 10**6
for instruction in instructions:
    args = instruction.split(' ')
    task = 'toggle' if args[0] == 'toggle' else args[1]
    if task == 'toggle':
        s, e = 1, 3
    else:
        s, e = 2, 4
    sx, sy = map(int, args[s].split(','))
    ex, ey = map(int, args[e].split(','))
    for y in range(sy, ey + 1):
        for x in range(sx, ex + 1):
            i = y * 1000 + x
            if task == 'toggle':
                lights[i] = not lights[i]
            else:
                lights[i] = task == 'on'
print('There are {} lights on.'.format(sum(1 for light in lights if light)))
lights = [0] * 10**6
for instruction in instructions:
    args = instruction.split(' ')
    task = 'toggle' if args[0] == 'toggle' else args[1]
    if task == 'toggle':
        s, e = 1, 3
    else:
        s, e = 2, 4
    sx, sy = map(int, args[s].split(','))
    ex, ey = map(int, args[e].split(','))
    d = {'toggle': 2, 'on': 1, 'off': -1}[task]
    for y in range(sy, ey + 1):
        for x in range(sx, ex + 1):
            lights[y * 1000 + x] = max(0, lights[y * 1000 + x] + d)
print('The total brightness is {}.'.format(sum(lights)))
