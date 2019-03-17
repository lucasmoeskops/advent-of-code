start = '1113122113'
end = start
def process(string):
    new = []
    i = 0
    while i < len(string):
        j = i + 1
        while j < len(string) and string[j] == string[i]:
            j += 1
        new.append(str(j - i) + string[i])
        i = j
    return ''.join(new)
for i in range(40):
    end = process(end)
print('After 40 iterations, the length of the result is {}.'.format(len(end)))
for i in range(10):
    end = process(end)
print('After 50 iterations, the length of the result is {}.'.format(len(end)))

