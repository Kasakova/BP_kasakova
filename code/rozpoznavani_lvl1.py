def load_config(config):
    with open(config, encoding="utf-8") as cfg:
        td_list = cfg.readlines()
    i = 0
    for word in td_list:
        word = word.lower()
        word = word.strip()
        print(word)
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


def rozpoznani(veta):
    veta = normalizace(veta)  # kdyby nahodou
    td = load_config('config.txt')
    tone = 'Tu'
    for word in td:
        if word in veta:
            tone = 'Td'
    return tone


print(rozpoznani('Jak se máš?'))


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
            line = normalizace(line)
            vety.append(line)
    for veta in vety:
        tone = rozpoznani(veta)
        rozp.append(tone)
