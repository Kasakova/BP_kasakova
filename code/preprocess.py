def erase_duplicates(file1, file2):
    """Seradi soubor podle abecedy a vymaze ty vety, ktere se opakuji"""
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
    return

def erase_divnou_notaci(file1, file2):
    """Zachova pouze text z vet s notaci."""
    with open(file1, encoding="utf-8") as f1:
        file_text = f1.readlines()
    with open(file2, 'w', encoding="utf-8") as f2:
        for line in file_text:
            if "(." in line:
                line = line.replace("(.", "")
                line = line.replace(")", "")
            f2.write(line)
    return

def petina(file, training, testing):
    """Ze souboru vytvori testovaci a trenovaci data v pomeru 20:80"""
    with open(file, encoding="utf-8") as f1, open(training, 'w', encoding="utf-8") as f2,open(testing, 'w', encoding="utf-8") as f3:
        file_text = f1.readlines()
        i = 1
        for line in file_text:
            if i % 5 == 0:
                f3.write(line)
            else:
                f2.write(line)
            i += 1
    return

if __name__ == '__main__':
    erase_divnou_notaci('data/questionsDE_s_notaci.txt', 'data/questionsDE.txt')

    erase_duplicates('data/questionsCZ.txt', 'data/sortedCZ_erased.txt')
    erase_duplicates('data/questionsEN.txt', 'data/sortedEN_erased.txt')
    erase_duplicates('data/questionsDE.txt', 'data/sortedDE_erased.txt')

    petina("data/sortedEN_erased.txt", "data/EN_training.txt", "data/EN_testing.txt")
    petina("data/sortedCZ_erased.txt", "data/CZ_training.txt", "data/CZ_testing.txt")
    petina("data/sortedDE_erased.txt", "data/DE_training.txt", "data/DE_testing.txt")
