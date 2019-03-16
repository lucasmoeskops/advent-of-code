strings = open('input.txt', 'r').read().strip().split('\n')
nice_strings = 0
for string in strings:
    vowels_required = 3
    double_found = False
    for i, char in enumerate(string):
        if char in 'aeiou':
            vowels_required -= 1
        if i > 0 and char == string[i - 1]:
            double_found = True
        if i > 0 and (char == 'b' and string[i - 1] == 'a' \
                or char == 'd' and string[i - 1] == 'c' \
                or char == 'q' and string[i - 1] == 'p' \
                or char == 'y' and string[i - 1] == 'x'):
            break
    else:
        if vowels_required < 1 and double_found:
            nice_strings +=  1
print('There are {} nice strings.'.format(nice_strings))
nice_strings = 0
for string in strings:
    repeat_found = False
    pair_found = False
    for i, char in enumerate(string):
        if not repeat_found and i > 1 and string[i - 2] == char:
            repeat_found = True
        if not pair_found and i > 2:
            for j, char2 in enumerate(string[0:i-2]):
                if string[i-1] + char == char2 + string[j+1]:
                    pair_found = True
        if repeat_found and pair_found:
            nice_strings += 1
            break
print('There are {} nice strings in the new system.'.format(nice_strings))

