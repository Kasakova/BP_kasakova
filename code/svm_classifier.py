from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from matplotlib import pyplot as plt
from freq_dict_training import normalizace
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def format_data(file):
    """Nacte data a anotace ze souboru do vektoru"""
    X, Y = [],[]
    with open(file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            line = line.split('\t')
            X.append(normalizace(line[0]))
            Y.append(line[1])
    return X,Y

def train_test(language):
    """Natrénuje a otestuje vybrany klasifikátor pro dany jazyk."""
    X, Y = format_data("data/"+language +"/train.txt")
    Xtest, Ytest = format_data("data/"+language +"/test.txt")
    # classifiers = [['tree', tree.DecisionTreeClassifier()],[],[],[]]
    classifier = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('svc', SVC(C=2, kernel="sigmoid")),
        # ('tree', tree.DecisionTreeClassifier()),
        # ('knn', KNeighborsClassifier(n_neighbors=1)),
        # ('5nn', KNeighborsClassifier(n_neighbors=5)),
    ])
    classifier.fit(X, Y)
    # fig = plt.figure(figsize=(25, 20))
    # _ = tree.plot_tree(classifier["tree"],
    #                    filled=True)
    # fig.savefig("decision_tree.svg")
    accuracy = 100 * round(classifier.score(Xtest, Ytest), 4)
    print(str(language), end="\t")
    print(f"{accuracy:.2f}" + ' %')
    return

def language_test(languages):
    """Otestuje klasifikátor pro vybrané jazyky"""
    for language in languages:
        train_test(language)
def SVC_param(language,start,step):
    """Otestuje svm klasifikator pro ruzne parametry C a kernel"""
    X, Y = format_data("data/"+language + "/train.txt")
    Xtest, Ytest = format_data("data/"+language + "/valid.txt")
    kernel = ["linear", "poly", "rbf", "sigmoid"]
    open('data.csv', "w").close()
    with open('data.csv', 'a', encoding='UTF8') as f:
        for k in range(len(kernel)):
            print(str(kernel[k]), end="\t")
            f.write(str(kernel[k]))
            if k != len(kernel) - 1:
                f.write(",")
        f.write("\n")
        print()
        for i in range(1,5):
            coef = round(start + i*step,3)
            print(str(coef), end="\t")
            f.write(str(coef) + ", ")
            for k in range(len(kernel)):
                ker = kernel[k]
                classifier = Pipeline([
                    ('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('svc', SVC(C=coef, kernel=ker)),
                ])
                classifier.fit(X, Y)
                accuracy = 100*round( classifier.score(Xtest, Ytest), 4)
                print(f"{accuracy:.2f}" + ' %', end="\t")
                f.write(f"{accuracy / 100:.4f}")
                if k != len(kernel)-1:
                    f.write(",")
            print()
            f.write("\n")
    print("\n")

def poly_test(languages):
    """Otestuje """
    open('data.csv', "w").close()
    with open('data.csv', 'a', encoding='UTF8') as f:
        for i in range(2,6):
            print(str(i), end="\t")
            f.write(str(i))
            if i != 5:
                f.write(",")
        print()
        f.write("\n")
        for language in languages:
            X, Y = format_data("data/" + language + "/train.txt")
            Xtest, Ytest = format_data("data/" + language + "/valid.txt")
            print(str(language), end="\t")
            f.write(str(language)+",")

            for i in range(2,6):
                classifier = Pipeline([
                    ('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('svc', SVC( kernel="poly", degree=i)),
                ])
                classifier.fit(X, Y)
                accuracy = 100 * round(classifier.score(Xtest, Ytest), 4)
                print(f"{accuracy:.2f}" + ' %', end="\t")
                f.write(f"{accuracy / 100:.4f}")
                if i != 5:
                    f.write(",")
            print()
            f.write("\n")
    print("\n")

if __name__ == '__main__':

    languages = ["CZ", "DE", "EN", "ES", "RU"]
    # language_test(languages)

    # SVC_param("CZ",0,1)
    SVC_param("CZ", 1.4, 0.2)
    # SVC_param("DE", 0, 1)
    # SVC_param("EN", 0, 1)
    # SVC_param("ES", 0, 1)
    # SVC_param("RU", 0, 1)

    csv = pd.read_csv("data.csv")
    # print(csv.style.to_latex(position_float="centering"))
    s = sns.heatmap(csv, annot=True, fmt=".2%")
    s.set(xlabel='Kernel', ylabel='Reg. koeficient')
    plt.show()

    # poly_test(languages)
    # csv = pd.read_csv("data.csv")
    # # print(csv.style.to_latex(position_float="centering"))
    # s = sns.heatmap(csv, annot=True, fmt=".2%")
    # s.set(xlabel='Stupeň polynomu', ylabel='Jazyk')
    # plt.show()

