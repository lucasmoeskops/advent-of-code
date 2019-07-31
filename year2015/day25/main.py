from re import search
from sys import argv

content = open('input.txt' if len(argv) < 2 else argv[1], 'r').read().strip()

row = int(search('row (\d+)', content).groups()[0])
column = int(search('column (\d+)', content).groups()[0])
start_code = 20151125

column_diagonal = row + column - 1
column_value = int((column_diagonal**2 + column_diagonal) / 2)
code_index = column_value - column_diagonal + column

final_code = start_code

for i in range(code_index - 1):
    final_code = 252533 * final_code % 33554393

print(f'The final code to enter is {final_code}.')
