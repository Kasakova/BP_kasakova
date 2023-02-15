import pandas as pd
from freq_dict_training import *
import yaml

def load_config(config):
    """Nacte konfiguracni yaml soubor a vrati slovnik se slovy pro Td a Tu"""
    with open(config, "r", encoding="UTF-8") as fr:
        data = yaml.full_load(fr)
    return data

def rozpoznani(veta,config, num):
    """Porovna, zda se mezi num prvnimi slovy vety nachazi slovo z configu a urci ton."""
    veta = normalizace(veta)
    td = config["Td"]
    tone = 'Tu'
    veta = veta.split()
    if num is not None:
        for i in range(min(num, len(veta))):
            if veta[i] in td:
                tone = 'Td'
                break
    else:
        for word in veta:
            if word in td:
                tone = 'Td'
                break
    return tone


def rozpoznani_souboru(file,config):
    """Pro cely soubor urci ton vety."""
    vety, anotace, rozp = [], [], []
    with open(file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if '?\t' in line:
                line = line.split('?\t')
            else:
                line = line.split('? ')

            anotace.append(line[-1])  # Tu/Td
            line.pop()

            ' '.join(line)
            line = line[0]
            line = normalizace(line)
            vety.append(line)
    conf = load_config(config)
    for veta in vety:
        tone = rozpoznani(veta,conf,2)
        rozp.append(tone)
    accuracy = vyhodnoceni(vety, rozp, anotace)
    return accuracy



def vyhodnoceni(vety, rozp, anotace):
    """Vyhodnoti presnost urcovani tonu."""
    count=0
    if len(rozp) == len(anotace):
        for i in range(len(rozp)):
            if rozp[i] == anotace[i]:
                count += 1
    accuracy = round(100*count/len(rozp),2)
    # print('Accuracy: ' + str(accuracy) + ' %')
    # confusion_matrix = pd.crosstab(anotace, rozp, rownames=['Actual'], colnames=['Predicted'])
    # print(confusion_matrix)
    print(str(accuracy) + ' %', end =" " )
    return accuracy

def config_test(trainfile,testfile,config,num,threshold,percentage ):
    """Vytvori konfiguracni soubor a ihned ho otestuje."""
    Td, Tu = freq_words(trainfile, num)
    make_config(Td, Tu, threshold,percentage,config)
    accuracy = rozpoznani_souboru(testfile, config)
    return accuracy

def test_parametry(trainfile, testfile):
    """Otestuje tvorbu konfiguracnich souboru pro ruzne parametry prahu."""
    open('data.csv', "w").close()
    with open('data.csv', 'a', encoding='UTF8') as f:
        k = 0.6
        f.write("\t")
        print("\t", end=" ")

        for j in range(3):
            print(str(k), end="\t")
            f.write(str(k)+ ", " )
            k += 0.1
            k = round(k, 1)
        print()
        f.write("\n")

        for i in range(2,5):
            k =0.6
            print(str(i), end =" ")
            f.write(str(i)+ ", " + " ")
            for j in range(3):
                accuracy = config_test(trainfile, testfile, "config/test.yaml", 2, i, k)
                f.write(str(accuracy) + " \%, ")
                k += 0.1
                k = round(k, 1)
            print()
            f.write("\n")
    return

if __name__ == '__main__':
    test_parametry('data/CZ_training.txt', 'data/CZ_testing.txt')

    # test_parametry('data/EN_training.txt', 'data/EN_testing.txt')
    import pandas as pd

    csv = pd.read_csv("data.csv")
    print(csv.style.to_latex(position_float="centering"))

    # rozpoznani_souboru('data/CZ_testing.txt', "config/handmadeCZ.yaml")
    #
    # rozpoznani_souboru('data/DE_testing.txt', "config/handmadeDE.yaml")
    #
    # rozpoznani_souboru('data/EN_testing.txt', "config/handmadeEN.yaml")




