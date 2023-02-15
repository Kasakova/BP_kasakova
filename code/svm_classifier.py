from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from freq_dict_training import normalizace

def format_data(file):
    """Nacte data a anotace ze souboru do vektoru"""
    X, Y = [],[]
    with open(file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            line = line.split('?\t')
            X.append(normalizace(line[0]))
            Y.append(line[1])
    return X,Y

def train_test(trainfile,testfile):
    X, Y = format_data(trainfile)
    Xtest, Ytest = format_data(testfile)
    classifier = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('svc', SVC()),
    ])
    classifier.fit(X, Y)
    print('Accuracy: ' + str(round(100 * classifier.score(Xtest, Ytest), 2)) + ' %')
    return

if __name__ == '__main__':
    train_test("data/CZ_training.txt", "data/CZ_testing.txt")
    train_test("data/EN_training.txt", "data/EN_testing.txt")
    train_test("data/DE_training.txt", "data/DE_testing.txt")
    train_test("data/ES_training.txt", "data/ES_testing.txt")
    train_test("data/RU_training.txt", "data/RU_testing.txt")



