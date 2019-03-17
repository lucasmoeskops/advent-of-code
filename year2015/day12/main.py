import json
data = json.load(open('input.txt', 'r'))
def find_values_sum(data):
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum(map(find_values_sum, data))
    if isinstance(data, dict):
        return sum(map(find_values_sum, data.values()))
    return 0
print('The sum of all values in the data is {}.'.format(find_values_sum(data)))
def find_values_sum_no_red(data):
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum(map(find_values_sum_no_red, data))
    if isinstance(data, dict):
        if 'red' in data.values():
            return 0
        return sum(map(find_values_sum_no_red, data.values()))
    return 0
print('The sum of all values in the data, ignoring red, is {}.'.format(
    find_values_sum_no_red(data)))
