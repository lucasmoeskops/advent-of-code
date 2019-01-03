from collections import Counter
from itertools import combinations
from sys import argv

passphrases = open(argv[1], 'r').read().strip().split('\n')


# Part 1

words = tuple(phrase.split(' ') for phrase in passphrases)
answer1 = sum(1 for phrase in words if len(phrase) == len(set(phrase)))
print('Number of valid passphrases is {} (from {} total phrases)'.format(
      answer1, len(passphrases)))


# Part 2

answer2 = sum(1
              for phrase in words
              if len(phrase) == len(set(''.join(sorted(word))
                                        for word in phrase)))
print('Number of valid passphrases is {} (from {} total phrases)'.format(
      answer2, len(passphrases)))
