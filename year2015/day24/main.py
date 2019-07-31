from functools import reduce
from itertools import combinations
from operator import itemgetter
from sys import argv


def find_minimum_entanglement(num_groups=3):
    num_packages = 1
    options = []
    group_weights = sum(weights) // num_groups

    while not options:
        if num_packages == 1:
            if group_weights in weights:
                options.append((group_weights),)
                break
        else:
            for combination in combinations(weights_reversed, num_packages - 1):
                combination_weight = sum(combination)
                missing_weight = group_weights - combination_weight

                if missing_weight < 0 or missing_weight > max_package:
                    continue

                if missing_weight in weights_reversed \
                        and missing_weight not in combination:
                    options.append(combination + (missing_weight,))

        num_packages += 1

    quantum_entanglements = {option: reduce(int.__mul__, option)
                             for option in options}

    # Now to find options that also allow for a division of the rest of the
    # packages
    sorted_by_entanglement = sorted(quantum_entanglements.items(),
                                    key=itemgetter(1))
    best_option = None
    for option, entanglement in sorted_by_entanglement:
        remaining_packages = set(weights) - set(option)
        rest_weights_rvrsd = tuple(sorted(remaining_packages, reverse=True))
        num_packages = 2  # 1 would be impossible: it would be in group 1

        while not best_option and num_packages <= len(remaining_packages) // (num_groups - 1):
            for combination in combinations(rest_weights_rvrsd, num_packages):
                if sum(combination) == group_weights:
                    best_option = option
                    break

            num_packages += 1

        if best_option:
            break

    return quantum_entanglements[best_option]


lines = open('input.txt'
             if len(argv) < 2 else argv[1], 'r').read().strip().split('\n')
# We assume that all weights are unique
weights = set(map(int, lines))

weights_reversed = tuple(sorted(weights, reverse=True))
max_package = weights_reversed[0]
minimum_quantum_entanglement = find_minimum_entanglement()
print(f'The minimum quantum entanglement is {minimum_quantum_entanglement}.')

# Part 2
minimum_quantum_entanglement = find_minimum_entanglement(4)
print(f'The minimum quantum entanglement using four groups is'
      f' {minimum_quantum_entanglement}.')
