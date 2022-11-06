import pandas as pd

def load_config(config):
    with open(config, encoding="utf-8") as cfg:
        td_list = cfg.readlines()
    i = 0
    for word in td_list:
        word = word.lower()
        word = word.strip()
        td_list[i] = word
        i += 1
    return td_list


def normalizace(veta):
    veta = veta.lower()
    veta = veta.replace(",", "")
    veta = veta.replace(".", "")
    veta = veta.replace("?", "")
    veta = veta.replace("-", "")
    veta = veta.replace("\n", "")
    veta = veta.replace("  ", " ")
    return veta

# #vyuziva substring
# def rozpoznani(veta,config):
#     veta = normalizace(veta)  # kdyby nahodou
#     td = config
#     tone = 'Tu'
#     for word in td:
#         if word in veta:
#             tone = 'Td'
#     return tone

# kontroluje po slovech
def rozpoznani(veta,config):
    veta = normalizace(veta)  # kdyby nahodou
    td = config
    tone = 'Tu'
    veta = veta.split()
    for ref in td:
        for word in veta:
            if word == ref:
                tone = 'Td'
    return tone

# # jen prvni slovo
# def rozpoznani(veta,config):
#     veta = normalizace(veta)  # kdyby nahodou
#     td = config
#     tone = 'Tu'
#     veta = veta.split()
#     for ref in td:
#         if veta[0] == ref:
#             tone = 'Td'
#     return tone


def rozpoznani_souboru(file):
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
    for veta in vety:
        tone = rozpoznani(veta,load_config('config.txt'))
        rozp.append(tone)
    return vety,rozp, anotace


vety,rozp, anotace = rozpoznani_souboru('CZ_testing.txt')
# vety,rozp, anotace = rozpoznani_souboru('EN_testing.txt')

def vyhodnoceni(vety, rozp, anotace):
    count=0
    if len(rozp) == len(anotace):
        for i in range(len(rozp)):
            if rozp[i] == anotace[i]:
                count += 1
            else:
                print(vety[i] + '\t' + anotace[i])
    else:
        print('Neco je spatne')
    print('Accuracy: ' + str(100*count/len(rozp)) + ' %')


vyhodnoceni(vety, rozp, anotace)


confusion_matrix = pd.crosstab(anotace, rozp, rownames=['Actual'], colnames=['Predicted'])
print(confusion_matrix)



