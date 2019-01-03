from itertools import combinations
from math import sqrt
from operator import itemgetter
from re import compile, match
from sys import argv

parser = compile(r'p=<(?P<px>-?\d+),(?P<py>-?\d+),(?P<pz>-?\d+)>, '
                  'v=<(?P<vx>-?\d+),(?P<vy>-?\d+),(?P<vz>-?\d+)>, '
                  'a=<(?P<ax>-?\d+),(?P<ay>-?\d+),(?P<az>-?\d+)>')
data = open(argv[1], 'r').read().strip().split('\n')
particles = tuple({
    'p': tuple(int(v) for v in (line['px'], line['py'], line['pz'])),
    'v': tuple(int(v) for v in (line['vx'], line['vy'], line['vz'])),
    'a': tuple(int(v) for v in (line['ax'], line['ay'], line['az'])),
} for line in (match(parser, line).groupdict() for line in data))


def size(vector):
    return sum(map(abs, vector))


def position_after(particle, steps):
    return tuple(p + int(.5 * steps * (2 * v + a * (steps + 1)))
                 for p, v, a in zip(particle['p'],
                                    particle['v'],
                                    particle['a']))


def onedimensional_clash(x1, v1, a1, x2, v2, a2):
    a = .5 * (a1 - a2)
    b = v1 - v2 + a
    c = x1 - x2
    d = b**2 - 4 * a * c
    if d < 0:
        return ()
    if a == 0:
        if b == 0:
            return (0,) if x1 == x2 else ()
        return int((x1 - x2) / (v2 - v1)),
    u1 = int((-b + sqrt(d)) / (2 * a))
    u2 = int((-b - sqrt(d)) / (2 * a))
    return (u1, u2)


# Part 1

slowest_acceleration = min(size(particle['a']) for particle in particles)
slowest_particles = tuple(particle
                          for particle in particles
                          if size(particle['a']) == slowest_acceleration)
lowest_position = min(size(position_after(particle, 100000000))
                      for particle in slowest_particles)
slowest_particles = (i
                     for i, particle in enumerate(particles)
                     if size(position_after(particle, 100000000)) == \
                             lowest_position)
answer1 = next(slowest_particles)
print('The particle closest to (0, 0, 0) is {}'.format(answer1)) 


# Part 2

particles_left = set(range(len(particles)))
clashes = {}
for id, other_id in combinations(range(len(particles)), 2):
    if not (id in particles_left and other_id in particles_left):
        continue
    particle = particles[id]
    other_particle = particles[other_id]
    # Calculate clashes in one dimension, and test for all dimensions
    x_clashes = onedimensional_clash(
            particle['p'][0],
            particle['v'][0],
            particle['a'][0],
            other_particle['p'][0],
            other_particle['v'][0],
            other_particle['a'][0])
    for clash in x_clashes:
        if clash >= 0:
            if position_after(particle, clash) == \
                    position_after(other_particle, clash):
                clashes[clash] = clashes.get(clash, set())
                clashes[clash].add((id, other_id))


for time, clashes_at in sorted(clashes.items(), key=itemgetter(0)):
    valid_clashes = tuple(clash
                          for clash in clashes_at
                          if clash[0] in particles_left \
                                  and clash[1] in particles_left)
    for clash in valid_clashes:
        particles_left -= set(clash)


answer2 = len(particles_left)
print('After collisions, {} particles are left'.format(answer2))

