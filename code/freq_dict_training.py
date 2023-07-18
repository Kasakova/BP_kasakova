import yaml

def normalizace(veta):
    """Ponecha z věty pouze znaky, ktere jsou soucasti slov."""
    veta = veta.lower()
    veta = veta.replace(",", "")
    veta = veta.replace(".", "")
    veta = veta.replace("?", "")
    veta = veta.replace("\n", "")
    veta = veta.replace("  ", " ")
    return veta

def split_data(file):
    """Rozdeli data do slovniku podle anotace"""
    dic = {"Td":[],"Tu": []}
    with open(file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            anot = line[-1]
            if '?\t' in line:
                line = line.split('?\t')
            else:
                line = line.split('? ')
            line = line[0]
            line = normalizace(line)
            if anot == "d":
                dic["Td"].append(line)
            if anot == "u":
                dic["Tu"].append(line)
    return dic

def freq_dict(wordlist):
    """Pro list slov vrati frekvencni slovnik vsech slov."""
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist, wordfreq)))



def dump_config(data,file):
    """Z parametru slovniku vytvori konfiguracni yaml soubor."""
    with open(file, "w", encoding="UTF-8") as fw:
        yaml.dump(data, fw, allow_unicode=True)
    return


def words(list, num=None):
    """Z listu vet vytvori list z prvnich num slov."""
    words= []
    for line in list:
        line = line.split(" ")
        if num is not None:
            for i in range(min(num, len(line))):
                words.append(line[i])
        else:
            for word in line:
                words.append(word)
    return words


def freq_words(file,num=None):
    """Vrati frekvencni slovniky pro oba tony z prvnich num slov vety."""
    Td = freq_dict(words(split_data(file)["Td"],num))
    Tu = freq_dict(words(split_data(file)["Tu"],num))
    return Td,Tu


def make_config(Td_freq, Tu_freq, threshold,percentage, file):
    """Z frekvencnich slovniku vytvori konfiguracni soubory."""
    config = {"Tu": [], "Td": []}
    for key in Td_freq:
        if Td_freq[key] > threshold:
            if key in Tu_freq:
                if Td_freq[key]/(Tu_freq[key]+Td_freq[key]) > percentage:
                    config["Td"].append(key)
            else:
                config["Td"].append(key)
    for key in Tu_freq:
        if Tu_freq[key] > threshold:
            if key in Td_freq:
                if Tu_freq[key]/(Tu_freq[key]+Td_freq[key]) > percentage:
                    config["Tu"].append(key)
            else:
                config["Tu"].append(key)
    dump_config(config, file)
    return


def new_cfg(file):
    """Vytvori z trenovacich dat optimalni konfiguracni soubor."""
    Td, Tu = freq_words(file, 2)
    language = file[file.find("/") + 1:file.find("/") + 3]
    make_config(Td, Tu, 2, 0.8, "config/" + language+".yaml")


if __name__ == '__main__':
    new_cfg("data/CZ/train.txt")
    new_cfg("data/DE/train.txt")
    new_cfg("data/EN/train.txt")
    new_cfg("data/ES/train.txt")
    new_cfg("data/RU/train.txt")
