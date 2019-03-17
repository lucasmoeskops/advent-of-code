start = 'hxbxwxba'
def increment_string(string):
    next_char = chr(ord(string[-1]) + 1)
    if next_char > 'z':
        return increment_string(string[:-1]) + 'a'
    return string[:-1] + next_char
def is_valid_password(string):
    double_found = False
    straight_found = False
    for char in ('i', 'l', 'o'):
        if char in string:
            return False
    pairs = []
    for i, char in enumerate(string[1:], start=1):
        if string[i - 1] == char and (not pairs or pairs[0] < i - 1):
            pairs.append(i)
            if len(pairs) == 2:
                break
    else:
        return False
    deltas = []
    for i, char in enumerate(string):
        deltas.append(ord(char))
        if i > 1 and deltas[i - 2] + 2 == deltas[i - 1] + 1 == deltas[i]:
            return True
    return False
string = start
while not is_valid_password(string):
    string = increment_string(string)
print('The first valid password is {}.'.format(string))
string = increment_string(string) 
while not is_valid_password(string):
    string = increment_string(string)
print('The next valid password is {}.'.format(string))
