strings = open('input.txt', 'r').read().strip().split('\n')
escaped_size = 0
def escaped_characters(string):
    if not string:
        return 0
    if string[0] == '"':
        return 1 + escaped_characters(string[1:])
    for i, char in enumerate(string):
        if char == '\\':
            if string[i + 1] == 'x':
                return 3 + escaped_characters(string[i + 4:])
            return 1 + escaped_characters(string[i + 2:])
        if char == '"':
            return 1
for string in strings:
    escaped_size += escaped_characters(string)
print('In total, {} characters are escape characters.'.format(escaped_size))
escape_size = 0
def escape_characters(string):
    if not string:
        return 0
    if string[0] == '"':
        return 2 + escape_characters(string[1:])
    for i, char in enumerate(string):
        if char == '\\':
            if string[i + 1] == 'x':
                return 1 + escape_characters(string[i+3:])
            return 2 + escape_characters(string[i+2:])
        if char == '"':
            return 2
for string in strings:
    escape_size += escape_characters(string)
print('In total, {} extra characters are needed.'.format(escape_size))
