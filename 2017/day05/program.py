from sys import argv

program = list(int(v) for v in open(argv[1], 'r').read().strip().split('\n'))


# Part 1

location = 0
answer1 = 0
program1 = program[:]
while 0 <= location < len(program1):
    next_step = location + program1[location]
    program1[location] += 1
    location = next_step
    answer1 += 1
print('The end of the program is reached after {} steps'.format(answer1))


# Part 2

location = 0
answer2 = 0
program2 = program
while 0 <= location < len(program2):
    value = program2[location]
    program2[location] = value + (1 if value < 3 else -1)
    location += value
    answer2 += 1
print('The end of the program is reached after {} steps'.format(answer2))
