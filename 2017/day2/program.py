from itertools import combinations
from sys import argv

rows = tuple(tuple(int(v) for v in line.split('\t'))
             for line in open(argv[1], 'r').read().strip().split('\n'))


# Part 1

answer1 = sum(max(row) - min(row) for row in rows)
print('The checksum of the spreadsheet is {}'.format(answer1))


# Part 2

answer2 = sum(j // i
              for row in rows
              for i, j in combinations(sorted(row), 2)
              if j % i == 0)
print('The sum of the divisions of the divisible values is {}'.format(answer2))

