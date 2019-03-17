from collections import Counter, defaultdict
lines = open('input.txt', 'r').read().strip().split('\n')
reindeer = {}
for line in lines:
    args = line.split(' ')
    reindeer[args[0]] = int(args[3]), int(args[6]), int(args[13])
distances = []
for speed, endurance, rest in reindeer.values():
    runtimes, remnant = int.__divmod__(2503, endurance + rest)
    distances.append((runtimes * endurance + min(endurance, remnant)) * speed)
print('Max distance travelled by a reindeer is {}.'.format(max(distances)))
points = Counter()
travelled = Counter()
for second in range(2503):
    for name, (speed, endurance, rest) in reindeer.items():
        if second % (endurance + rest) < endurance:
            travelled[name] += speed
    points[travelled.most_common(1)[0][0]] += 1
print('The reindeer with the most points has {} points.'.format(
    max(points.values())))
