def sort_alphabetically(file1, file2):
    with open(file1, encoding="utf-8") as file:
        file_text = file.readlines()
    file_text.sort()
    with open(file2, 'w', encoding="utf-8") as f:
        for line in file_text:
            f.write(line)


# sort_alphabetically('questionsCZ.txt', 'sortedCZ.txt')
# sort_alphabetically('questionsEN.txt', 'sortedEN.txt')
# sort_alphabetically('questionsDE.txt', 'sortedDE.txt')


def erase_duplicates(file1, file2):
    with open(file1, encoding="utf-8") as file:
        file_text = file.readlines()
    file_text.sort()
    with open(file2, 'w', encoding="utf-8") as f:
        prev_sentence = ""
        for line in file_text:
            sentence = line.split('/t')
            if sentence[0] != prev_sentence:
                f.write(line)
            prev_sentence = sentence[0]


erase_duplicates('questionsCZ.txt', 'sortedCZ_erased.txt')
erase_duplicates('questionsEN.txt', 'sortedEN_erased.txt')
erase_duplicates('questionsDE.txt', 'sortedDE_erased.txt')