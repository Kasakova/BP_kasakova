from itertools import islice


# def split_50_50(file, even, odd):
#     with open(file) as f1, open(even, 'w') as f2:
#         for line in islice(f1, 0, None, 2):
#             f2.write(line)
#     with open(file) as f1, open(odd, 'w') as f2:
#         for line in islice(f1, 1, None, 2):
#             f2.write(line)
#
#
# def split_75_25(file, training, testing ):
#     split_50_50(file, training, 'odds.txt')
#     split_50_50('odds.txt', training,testing)


def petina(file, training, testing):
    with open(file, encoding="utf-8") as f1, open(training, 'w', encoding="utf-8") as f2,open(testing, 'w', encoding="utf-8") as f3:
        file_text = f1.readlines()
        i = 1
        for line in file_text:
            if i % 5 == 0:
                f3.write(line)
            else:
                f2.write(line)
            i += 1


petina("sortedEN_erased.txt", "EN_training.txt", "EN_testing.txt")
petina("sortedCZ_erased.txt", "CZ_training.txt", "CZ_testing.txt")
# petina("sortedDE_erased.txt", "DE_training.txt", "DE_testing.txt")
