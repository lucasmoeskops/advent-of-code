from collections import Counter
from sys import argv
from random import randint

box_ids = open(argv[1], 'r').read().split('\n')[:-1]

# Part 1

def occurrence_counter(times):
    return sum(1 for letter_count in letter_counts if times in letter_count)

letter_counts = tuple(set(counter.values())
                      for counter in map(Counter, box_ids))
answer1 = occurrence_counter(2) * occurrence_counter(3)
print('The checksum is: {}'.format(answer1))


# Part 2

columns = tuple(zip(*box_ids))
options = (columns[:i] + columns[i + 1:] for i in range(len(columns)))
best_match = (Counter(zip(*option)).most_common(1)[0] for option in options)
answer2 = ''.join(next(match
                       for match, times_found in best_match
                       if times_found == 2))
print('Matching characters are: {}'.format(answer2))

