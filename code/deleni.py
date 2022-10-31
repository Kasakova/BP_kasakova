from itertools import islice
with open('sortedEN_erased.txt') as f1, open('evens.txt', 'w') as f2:
    for line in islice(f1, 0, None, 2):
        f2.write(line)

with open('sortedEN_erased.txt') as f1, open('odds.txt', 'w') as f2:
    for line in islice(f1, 1, None, 2):
        f2.write(line)