from collections import defaultdict
from sys import argv
lines = open('input.txt' if len(argv) < 2 else argv[1], 'r').read().strip().split('\n')
target = lines.pop()
lines.pop()
replacements = defaultdict(list)
for line in lines:
    from_, _, to_ = line.strip().split(' ')
    replacements[from_].append(to_)
new_molecules = set()
for from_ in replacements:
    for to_ in replacements[from_]:
        for i in range(len(target) - len(from_) + 1):
            if target[i:i+len(from_)] == from_:
                new_molecules.add(target[:i] + to_ + target[i+len(from_):])
print('There can be made {} different molecules after one iteration.'.format(
    len(new_molecules)))
# Let's find results that have multiple options
results = set()
duplicates = set()
for from_, tos in replacements.items():
    for to in tos:
        for result in results:
            if to in result:
                duplicates.add(to)
            if result in to:
                duplicates.add(result)
        results.add(to)
if duplicates:
    print('We assumed there were no duplicates. Sorry')
    quit()
# So, no duplicates. Now we can make replacements, but the order might
# matter. To make order not matter, let's start at the end (or the
# beginning would be another option). Also not every part might be
# replaceable immediately, so we add a skip factor if we can't find a
# replacement.
# First we need a backwards lookup for results.
rev_replacements = {}
for from_, tos in replacements.items():
    for to in tos:
        # We already know the replacement is unique
        rev_replacements[to] = from_
# Now we can look for matching replacements
num_replacements = 0
query_size = 1
skip_chars = 0
while query_size <= len(target) and skip_chars < len(target):
    while query_size + skip_chars <= len(target):
        slice_end = -skip_chars if skip_chars else len(target)
        snippet = target[-query_size - skip_chars:slice_end]
        if snippet in rev_replacements:
            before = len(target)
            target = target[:-query_size - skip_chars] + rev_replacements[snippet] + target[slice_end:]
            num_replacements += 1
            query_size = 1
            skip_chars = 0
        else:
            query_size += 1
    skip_chars += 1
    query_size = 1
# The target should now be the starting value, 'e'
if target != 'e':
    print(f'Something went wrong with the replacements. We got \'{target}\''
          f' instead of \'e\'')
    quit()
print(f'The fewest number of steps to arrive at \'e\' is {num_replacements}.')
