from itertools import chain
from sys import argv

number = open(argv[1], 'r').read().strip()


# Part 1

answer1 = sum(int(m)
              for m, n in zip(number, chain(number[1:], number[:1]))
              if m == n)
print('Captcha sum is {}'.format(answer1))


# Part 2

o = len(number) // 2
answer2 = sum(int(m)
              for m, n in zip(number, chain(number[o:], number[:o]))
              if m == n)
print('Captcha sum is {}'.format(answer2))
