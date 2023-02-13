def erase_duplicates(file1, file2):
    """Seradi soubor podle abecedy a vymaze ty vety, ktere se opakuji"""
    with open(file1, encoding="utf-8") as file:
        file_text = file.readlines()
    file_text.sort()
    with open(file2, 'w', encoding="utf-8") as f:
        prev_sentence = ""
        for line in file_text:
            sentence = line.split('\t')
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

def erase_ipa(file1,file2):
    with open(file1, encoding="utf-8") as file:
        file_text = file.readlines()
    with open(file2, 'w', encoding="utf-8") as f:
        for line in file_text:
            tone = None
            line = line[9:-1]
            if "<Td>" in line:
                tone = "Td"
            elif "<Tu>" in line:
                tone = "Tu"
            if "?" in line:
                while "[" in line:
                    line = line[0:line.index("[")] + line[line.index("]") + 1:]
                line = line[0:line.index("?")+1]
                if tone is not None:
                    line = line.replace("…","")
                    line = line.replace("¿","")
                    line = line.replace("`", "")
                    line+= "\t" + tone
                    f.write(line +"\n")



if __name__ == '__main__':
    # erase_divnou_notaci('data/questionsDE_s_notaci.txt', 'data/questionsDE.txt')
    erase_ipa("data/ES_annot.ipa.snt", "data/questionsES.txt")
    erase_ipa("data/RU_annot.ipa.snt", "data/questionsRU.txt")
    #
    # erase_duplicates('data/questionsCZ.txt', 'data/sortedCZ_erased.txt')
    # erase_duplicates('data/questionsEN.txt', 'data/sortedEN_erased.txt')
    # erase_duplicates('data/questionsDE.txt', 'data/sortedDE_erased.txt')
    erase_duplicates('data/questionsES.txt', 'data/sortedES_erased.txt')
    erase_duplicates('data/questionsRU.txt', 'data/sortedRU_erased.txt')
    #
    # petina("data/sortedEN_erased.txt", "data/EN_training.txt", "data/EN_testing.txt")
    # petina("data/sortedCZ_erased.txt", "data/CZ_training.txt", "data/CZ_testing.txt")
    # petina("data/sortedDE_erased.txt", "data/DE_training.txt", "data/DE_testing.txt")
    petina("data/sortedES_erased.txt", "data/ES_training.txt", "data/ES_testing.txt")
    petina("data/sortedRU_erased.txt", "data/RU_training.txt", "data/RU_testing.txt")
