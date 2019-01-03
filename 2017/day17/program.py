from sys import argv

step = int(argv[1]) if len(argv) > 1 else 349


class Node:
    def __init__(self, value):
        self.value = value
        self.before = self 
        self.after = self


def insert_after(after_node, node):
    before_node = after_node.after
    node.before = after_node
    node.after = before_node
    after_node.after = node
    before_node.before = node


def step_from(node, n):
    while n != 0:
        if n > 0:
            node = node.after
            n -= 1
        else:
            node = node.before
            n += 1
    return node


def run(base, steps):
    current_position = base
    prev = 0
    for i in range(steps):
        new = Node(i + 1)
        insert_after(step_from(current_position, step), new)
        current_position = new
    return current_position


def determine_after_zero(steps):
    # Inspired by https://github.com/CameronAavik/AdventOfCode/blob/master/Challenges/2017/Day17.fs
    p = 0
    v = 0
    for i in range(1, steps + 2):
        p = (p + 1) % i
        if p == 1:
            v = i - 1
        p = (p + step) % i
    return v


# Part 1

base = Node(0)
current_position = run(base, 2017)
answer1 = step_from(current_position, 1).value
print('The value immediately after the last value written (2017) is {}'.format(
      answer1))


# Part 2

answer2 = determine_after_zero(5 * 10**7)
print('The value immediately after 0 after 50 million values is {}'.format(
      answer2))
