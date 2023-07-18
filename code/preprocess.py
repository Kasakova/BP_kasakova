from sklearn.model_selection import train_test_split
import os
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

def erase_notaci(file1, file2):
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

def erase_ipa(file1,file2):
    """Vymaze z dat fonetickou transkripci slov."""
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
                    line += "\t" + tone
                    f.write(line + "\n")

def csv_to_tsv(file1,file2):
    with open(file1, encoding="utf-8") as file:
        file_text = file.readlines()
    with open(file2, 'w', encoding="utf-8") as f:
        for line in file_text:
            line = line.split(";")
            for i in range(len(line)):
                 line[i]= line[i].strip()
            f.write(line[1]+"\t"+line[0]+"\n")

def train_test_validate(file):
    """Rozdeli data na trenovaci, testovaci, validacni."""
    print(file.rfind("/"))
    language = file[file.rfind("/")+1:file.rfind("/")+3]
    print(language)
    with open(file, encoding="utf-8") as file:
        file_text = file.readlines()
    train, test = train_test_split(file_text, test_size=0.2)
    train, val = train_test_split(train, test_size=0.1)
    print(len(train))
    try:
        os.mkdir("data/"+language)
    except FileExistsError:
        print("Slozka jiz existuje.")
    with open("data/"+language+"/train.txt", 'w+', encoding="utf-8") as file:
        file.writelines(train)
    with open("data/"+language+"/test.txt", 'w+', encoding="utf-8") as file:
        file.writelines(test)
    with open("data/"+language+"/valid.txt", 'w+', encoding="utf-8") as file:
        file.writelines(val)
    print(len(test))
    print(len(val))

if __name__ == '__main__':
    # erase_notaci('data/questionsDE_s_notaci.txt', 'data/questionsDE.txt')
    # erase_ipa("data/ES_annot.ipa.snt", "data/questionsES.txt")
    # csv_to_tsv("data/RU_questions.csv", "data/questionsRU.txt")

    #
    erase_duplicates('data/questionsCZ.txt', 'data/CZ.txt')
    erase_duplicates('data/questionsEN.txt', 'data/EN.txt')
    erase_duplicates('data/questionsDE.txt', 'data/DE.txt')
    erase_duplicates('data/questionsES.txt', 'data/ES.txt')
    erase_duplicates('data/questionsRU.txt', 'data/RU.txt')
    #
    # petina("data/sortedEN_erased.txt", "data/EN_training.txt", "data/EN/test.txt",5)
    # petina("data/sortedCZ_erased.txt", "data/CZ_training.txt", "data/CZ/test.txt",5)
    # petina("data/sortedDE_erased.txt", "data/DE_training.txt", "data/DE/test.txt",5)
    # petina("data/sortedES_erased.txt", "data/ES_training.txt", "data/ES/test.txt",5)
    # petina("data/sortedRU_erased.txt", "data/RU_training.txt", "data/RU/test.txt",5)

    # train_test_validate("data/CZ.txt")
    # train_test_validate("data/EN.txt")
    # train_test_validate("data/DE.txt")
    # train_test_validate("data/ES.txt")
    # train_test_validate("data/RU.txt")