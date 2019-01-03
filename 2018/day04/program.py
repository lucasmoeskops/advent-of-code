from collections import Counter
from itertools import chain, groupby, islice, zip_longest
from operator import itemgetter
from re import compile, match
from sys import argv


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


parser = compile(r'\[(?P<date>[^\]]+)\] (Guard (?P<ID>#\d+) )?(?P<action>.+)$')
data = tuple(match(parser, line).groupdict()
             for line in open(argv[1], 'r').read().strip().split('\n'))


# Part 1


def get_minute(date):
    return int(date[-2:])


def asleep_ranges(guard_entries):
    return (range(get_minute(start['date']), get_minute(end['date']))
            for start, end in grouper(guard_entries, 2))


chronological = sorted(data, key=itemgetter('date'))
shift_swaps = tuple(index
                    for index, entry in enumerate(chronological)
                    if entry['ID'])
shift_ranges = zip(shift_swaps, chain(islice(shift_swaps, 1, None), (None,))) 
per_shift = tuple((chronological[start]['ID'], chronological[start + 1:end])
                  for start, end in shift_ranges)
per_guard = groupby(sorted(per_shift, key=itemgetter(0)), key=itemgetter(0))
guard_asleep = tuple((k, Counter(
                        chain.from_iterable(
                            asleep_ranges(
                                chain.from_iterable(
                                    shift[1] for shift in v)))))
                for k, v in per_guard)
most_asleep = sorted(guard_asleep, key=lambda g: -sum(g[1].values()))[0]
most_asleep_minute = most_asleep[1].most_common(1)[0][0]
answer1 = int(most_asleep[0][1:]) * most_asleep_minute
print('The ID of the guard multiplied by the minute is {}'.format(answer1))


# Part 2

most_asleep_minutes = ((guard, asleep.most_common(1)[0])
                       for guard, asleep in guard_asleep
                       if asleep)
most_asleep_minute = sorted(most_asleep_minutes, key=lambda g: -g[1][1])[0]
answer2 = int(most_asleep_minute[0][1:]) * most_asleep_minute[1][0]
print('The ID of the guard multiplied by the minute is {}'.format(answer2))

