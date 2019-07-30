from collections import defaultdict, deque, Counter
lines = open('input.txt', 'r').read().strip().split('\n')
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
rev_replacements = []
for from_, tos in replacements.items():
    for to in tos:
        rev_replacements.append((to, from_))
uniqueness = Counter()
for to, from_ in rev_replacements:
    uniqueness.update(to)
rev_replacements.sort(key=lambda x: (-min(uniqueness[c] for c in x[0]), x[0]),
                      reverse=True)
def find_origin(molecule):
    def recurse(steps, premolecule):
        print(premolecule)
        #if premolecule in known:  # and steps > known[premolecule]:
        #    return
        #known[premolecule] = steps
        if premolecule == 'e':
            return steps
        for to, from_ in rev_replacements:
            found = False
            while to in premolecule:
                steps += 1
                premolecule = premolecule.replace(to, from_, 1)
                found = True
            if found:
                stack.append((
                    steps,
                    premolecule))
                    #premolecule[:i] + from_ + premolecule[i+len(to_):]))
                break
    stack = [(0, molecule)]
    known = set()
    results = []
    p = 1000
    while stack:
        p -= 1
        if p == 0:
            print(len(stack), stack[-1][0], len(stack[-1][1]))
            p = 1000
#        best_option = min(stack, key=lambda x: len(x[1]))
#        if best_option[1] in known:
#            stack.remove(best_option)
#            continue
#        else:
#            known.add(best_option[1])
        result = recurse(*stack.pop())
        if isinstance(result, int):
            results.append(result)
    return min(results)
print('The fastest way to make the molecules takes {} steps.'.format(
    find_origin(target)))
