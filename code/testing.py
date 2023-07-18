import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from freq_dict_training import *
import yaml


def load_config(config):
    """Nacte konfiguracni yaml soubor a vrati slovnik se slovy pro Td a Tu"""
    with open(config, "r", encoding="UTF-8") as fr:
        data = yaml.full_load(fr)
    return data


def rozpoznani(veta,config, Tu = False,numTu=None,numTd=2):
    """Porovna, zda se mezi num prvnimi slovy vety nachazi slovo z configu a urci ton."""
    veta = normalizace(veta)
    td = config["Td"]
    tone = 'Tu'
    veta = veta.split()
    if numTd is not None:
        for i in range(min(numTd, len(veta))):
            if veta[i] in td:
                tone = 'Td'
                return tone
    else:
        for word in veta:
            if word in td:
                tone = 'Td'
                return tone

    if Tu == True:
        tu = config["Tu"]
        tone = 'T?'
        if numTu is not None:
            for i in range(min(numTu, len(veta))):
                if veta[i] in tu:
                    tone = 'Tu'
                    return tone
        else:
            for word in veta:
                if word in tu:
                    tone = 'Tu'
                    return tone
    return tone


def rozpoznani_souboru(file,config,printm=False,Tu=False,numTd=2,numTu=None):
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
        tone = rozpoznani(veta,conf,Tu,numTu,numTd)
        rozp.append(tone)
    accuracy = vyhodnoceni(vety, rozp, anotace,printm)
    return accuracy


def vyhodnoceni(vety, rozp, anotace,printm):
    """Vyhodnoti presnost urcovani tonu."""
    count=0
    if len(rozp) == len(anotace):
        for i in range(len(rozp)):
            if rozp[i] == anotace[i]:
                count += 1
            # else:
            #     print(vety[i] + " " + anotace[i])
    accuracy = round(100*count/len(rozp),2)
    # print('Accuracy: ' + str(accuracy) + ' %')
    if printm==True:
        confusion_matrix = pd.crosstab(anotace, rozp, rownames=['Actual'], colnames=['Predicted'])
        print(confusion_matrix)
    return accuracy


def config_test(trainfile, testfile, config, num, threshold, percentage):
    """Vytvori konfiguracni soubor a ihned ho otestuje."""
    Td, Tu = freq_words(trainfile,num)
    make_config(Td, Tu, threshold,percentage,config)
    accuracy = rozpoznani_souboru(testfile, config,False,False,numTd=2)
    return accuracy


def test_parametry(trainfile, testfile):
    """Otestuje tvorbu konfiguracnich souboru pro ruzne parametry prahu."""
    open('data.csv', "w").close()
    with open('data.csv', 'a', encoding='UTF8') as f:
        k = 0.6
        # f.write("\t")
        print("\t", end=" ")

        for j in range(4):
            print(str(k), end="\t")
            f.write(str(k))
            if j != 3:
                f.write(",")
            k += 0.1
            k = round(k, 1)
        print()
        f.write("\n")

        for i in range(6):
            k =0.6
            print(str(i), end ="\t")
            f.write(str(i)+ ", " + " ")
            for j in range(1,5):
                accuracy = config_test(trainfile, testfile, "config/test.yaml", 2, i, k)
                print(f"{accuracy:.2f}", end="\t")
                f.write(f"{accuracy/100:.4f}")
                if j != 4:
                    f.write(",")
                k += 0.1
                k = round(k, 1)
            print()
            f.write("\n")
    return


def cfm_test(languages):
    """Otestuje rucne vytvorene konfiguracni soubory pro vsechny kombinace poctu poc. slov"""
    for language in languages:
        konfigurace =[[True,1,1],[True,2,1],[True,2,2],[False,2,0],[False,3,0]]
        print(language, end="\t")
        for k in konfigurace:
            accuracy = round(rozpoznani_souboru("data/"+language+"/valid.txt", "config/handmade"+language+".yaml", True,k[0],k[1],k[2]), 2)
        print()


def handmade_test(languages):
    """Otestuje rucne vytvorene konfiguracni soubory pro vsechny pozadovane jazyky na 1-3 počátečních slovech."""
    open('data.csv', "w").close()
    with open('data.csv', 'a', encoding='UTF8') as f:
        print("\t", end=" ")

        for k in range(0, 4):
            if k == 0:
                print("vše", end="\t")
                f.write("vše")
            else:
                print(str(k), end="\t")
                f.write(str(k))
            if k != 3:
                f.write(",")
        print()
        f.write("\n")

        for language in languages:
            print(language, end="\t")
            f.write(language + ", " + " ")
            for j in range(0, 4):
                if j == 0:
                    accuracy = round(
                        rozpoznani_souboru("data/" + language + "/valid.txt", "config/handmade" + language + ".yaml", False, False), 2)
                else:
                    accuracy = round(rozpoznani_souboru("data/"+language+"/valid.txt", "config/handmade"+language+".yaml", False,False, j), 2)
                print(f"{accuracy:.2f}", end="\t")
                f.write(f"{accuracy/100:.4f}")
                if j != 3:
                    f.write(",")
            print()
            f.write("\n")


def opt_test(languages):
    """Otestuje optimalne vytvorene konfiguracni soubory pro vsechny pozadovane jazyky na 2 pocatecnich slovech."""
    open('data.csv', "w").close()
    with open('data.csv', 'a', encoding='UTF8') as f:
        for language in languages:
            print(language, end="\t")
            f.write(language + ", " + " ")
            accuracy = round(rozpoznani_souboru("data/"+language+"/test.txt", "config/"+language+".yaml", False,False,2), 2)
            print(f"{accuracy:.2f}", end="\t")
            f.write(f"{accuracy/100:.4f}")
            print()
            f.write("\n")


if __name__ == '__main__':
    lang = ["CZ", "DE", "EN", "ES", "RU"]
    hand_lang = ["CZ", "EN", "DE", "ES"]
    # cfm_test(["EN"])
    # handmade_test(hand_lang)

    # csv = pd.read_csv("data.csv")
    # # print(csv.style.to_latex(position_float="centering"))
    # s = sns.heatmap(csv, annot=True, fmt=".2%")
    # s.set(xlabel='Počátečních slov', ylabel='Jazyk')
    # plt.show()

    # test_parametry('data/CZ/train.txt', 'data/CZ/valid.txt')
    # test_parametry('data/DE/train.txt', 'data/DE/valid.txt')
    # test_parametry('data/EN/train.txt', 'data/EN/valid.txt')
    # test_parametry('data/ES/train.txt', 'data/ES/valid.txt')
    # test_parametry('data/RU/train.txt', 'data/RU/valid.txt')

    # csv = pd.read_csv("data.csv")
    # s = sns.heatmap(csv, annot=True, fmt=".2%")
    # s.set(xlabel='Min. poměr', ylabel='Min. počet')
    # plt.show()

    # opt_test(lang)

    # rozpoznani_souboru("data/EN/valid.txt", "config/handmadeEN.yaml", printm=True, Tu=True, numTd=2, numTu=2)
