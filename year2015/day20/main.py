# Kind of factorial sums times 10
from math import ceil

target_number = 34000000
# Remove the 10, it's just noise
factorial_sum = target_number // 10
# The houses getting the most presents are the ones with the most matching
# factors. It's hard to point to a specific limit, so we'll do an
# exhaustive approach. As a simple limit to the search we can take the
# (factorial_sum + 1) / 2, rounded down, since the factorial sum
# of 2^n is 2^(n + 1) - 1.
limit = (factorial_sum + 1) // 2 + 1  # + 1 since it is not inclusive
sums = [1] * limit  # We already know it's at least 1
house = 1
for elf in range(2, limit):
    for sum in range(elf, limit, elf):
        sums[sum - 1] += elf
    if sums[elf - 1] >= factorial_sum:
        house = elf
        break
print(f'The first house getting at least {target_number} presents is'
      f' #{house}.')
# For the second part, we can divide by 11 as factor. Also instead of
# updating the whole array, we only need to update max 50 times per elf
factorial_sum = ceil(target_number / 11)
limit = (factorial_sum + 1) // 2 + 1  # + 1 since it is not inclusive
sums = [1] * limit  # We already know it's at least 1
for elf in range(2, limit):
    for sum in range(elf, min(limit, elf * 51), elf):
        sums[sum - 1] += elf
    if sums[elf - 1] >= factorial_sum:
        house = elf
        break
print(f'The first house now getting at least {target_number} presents is'
      f' #{house}.')
