import csv


# metoda wenątrzna której zadaniem jest czytanie pliku celem dalszej obróbki
def readfile(filepath, delimiter=';'):
    with open(filepath, newline='') as plik:
        dane = list(csv.reader(plik, delimiter=delimiter))
        if len(dane[-1]) != len(dane[-2]):
            dane.pop()
        return dane


def create_dict_from_file(filepath) -> dict:
    with open(filepath, newline='') as plik:
        return {wiersz.replace("\n", ""): i for i, wiersz in enumerate(plik)}


# metoda która dzieli mi dane na zbiory testowy i treningowy
def splitcsvdata(filepath, trainfilepath="trainData.csv", testfilepath="testData.csv", testowe=10):
    try:
        dane = readfile(filepath)
    except FileNotFoundError:
        print("Nie odnaleziono pliku")
        return

    attrdecyzyjne = dict()
    for wyraz in dane:
        if attrdecyzyjne.get(wyraz[-1]) is None:
            attrdecyzyjne[wyraz[-1]] = list()

        attrdecyzyjne.get(wyraz[-1]).append(wyraz[:-1])

    # dokonuję podziału zbioru danych na testowe i treningowe
    with open(trainfilepath, 'w', newline='') as csvtrainfile, open(testfilepath, 'w', newline='') as csvtestfile:
        trainwriter = csv.writer(csvtrainfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        testwriter = csv.writer(csvtestfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for decisionattr in attrdecyzyjne.keys():

            for singledata in attrdecyzyjne.get(decisionattr)[:testowe]:
                trainwriter.writerow(singledata + [decisionattr])

            for singledata in attrdecyzyjne.get(decisionattr)[testowe:]:
                testwriter.writerow(singledata + [decisionattr])
    return f"Dane treningowe podzielone na: {testowe} danych z każdej grupy jako trening, pozostałe jako testowe"
