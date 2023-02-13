import pandas as pd
from freq_dict_training import normalizace
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
    tu = config["Tu"]
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
    vyhodnoceni(vety, rozp, anotace)
    return



def vyhodnoceni(vety, rozp, anotace):
    """Vyhodnoti presnost urcovani tonu."""
    count=0
    if len(rozp) == len(anotace):
        for i in range(len(rozp)):
            if rozp[i] == anotace[i]:
                count += 1
            # else:
            #     print(vety[i] + '\t' + anotace[i])
    else:
        print('Neco je spatne')
    print('Accuracy: ' + str(100*count/len(rozp)) + ' %')
    confusion_matrix = pd.crosstab(anotace, rozp, rownames=['Actual'], colnames=['Predicted'])
    print(confusion_matrix)


if __name__ == '__main__':
    rozpoznani_souboru('data/CZ_testing.txt', "config/handmadeCZ.yaml")

    rozpoznani_souboru('data/DE_testing.txt', "config/handmadeDE.yaml")

    rozpoznani_souboru('data/EN_testing.txt', "config/handmadeEN.yaml")




