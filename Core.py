import math
import re

from Biblioteki import MenuInterface, readfile, create_dict_from_file, splitcsvdata


class Core:
    nazwa = {0: "SPAM", 1: "NIE SPAM"}

    def __init__(self, parent: MenuInterface, trainFilePath: str = None, wordsDictPath: str = None):
        self.parent = parent
        self.iloscPrzypadkow = dict()
        self.traindata = list()
        self.wordsDict = None
        if trainFilePath is not None:
            self.traindata = readfile(trainFilePath, delimiter=",")
            self._preprocess_data()
        if wordsDictPath is not None:
            self.wordsDict = create_dict_from_file(wordsDictPath)

        self.parent.changeinfo(str(self))

    def __str__(self):
        return "\n".join([f"Przypadek: {item[0]} ilosc: {item[1]}" for item in self.iloscPrzypadkow.items()])

    def _preprocess_data(self):
        for wiersz in self.traindata:
            expected = int(wiersz[-1])
            if self.iloscPrzypadkow.get(expected) is None:
                self.iloscPrzypadkow[expected] = 0
            self.iloscPrzypadkow[expected] += 1

    def test(self):
        self.parent.showdata("Test png", important=True)

    def podziel_dane(self):

        original , cancel = self.parent.collectdata("Podział danych","Podaj ścieżkę do oryginalnego pliku csv")
        if cancel:
            return
        trainpath, cancel = self.parent.collectdata("Podział danych","Podaj ścieżkę do oryginalnego pliku csv")
        if cancel:
            return
        testpath, cancel = self.parent.collectdata("Podział danych","Podaj ścieżkę do oryginalnego pliku csv")
        if cancel:
            return
        iloscTestowych, cancel = self.parent.collectdata("Podział danych","Podaj ścieżkę do oryginalnego pliku csv")
        if cancel:
            return
        result = splitcsvdata(
            filepath=original,
            trainfilepath=trainpath,
            testfilepath=testpath,
            testowe=int(iloscTestowych)
        )
        self.parent.showdata(outputdata=result, important=True)

    @staticmethod
    def _prepare_table(data, ilosc_wystapien: int):
        result = [
            math.log(element / ilosc_wystapien) if element > 0 else math.log((element + 1) / (ilosc_wystapien + 2))
            for element in data]
        return result

    def _ocen_core(self, data: list):
        tablice = {klucz: [0] * len(self.wordsDict) for klucz in self.iloscPrzypadkow.keys()}

        for wiersz in self.traindata:
            for i, wektor in enumerate(wiersz[:-1]):
                if int(wektor) == int(data[i]):
                    tablice.get(int(wiersz[-1]))[i] += 1

        for klucz in tablice.keys():
            tablice[klucz] = self._prepare_table(tablice[klucz], ilosc_wystapien=self.iloscPrzypadkow[klucz])

        wyniki = dict()
        for klucz in self.iloscPrzypadkow.keys():
            pY = self.iloscPrzypadkow.get(klucz) / len(self.traindata)
            wyniki[klucz] = sum(tablice[klucz]) + math.log(pY)

        return sorted(wyniki.items(), key=lambda x: x[1], reverse=True)[0][0]

    def ocen(self):

        test, cancel = self.parent.collectdata("Ocena", "Skopiuj tu treść emaila do oceny")
        if cancel:
            return

        test = re.sub(r'[^\w]', ' ', re.sub(r' +', ' ', test))

        converted = [0] * (len(self.wordsDict))
        for slowo in test.split(" "):
            numer = self.wordsDict.get(slowo)
            if numer is not None:
                converted[numer] = 1

        self.parent.showdata(Core.nazwa.get(self._ocen_core(converted)), important=True)

    def skutecznosc(self):

        testFiele, cancel = self.parent.collectdata("Testy", "Podaj ścieżkę do pliku testowego")

        if cancel:
            return

        daneTestowe = readfile(testFiele, delimiter=",")

        macierz = {0: {0: 0, 1: 0}, 1: {0: 0, 1: 0}}
        for test in daneTestowe:
            ocena = int(self._ocen_core(test[:-1]))
            macierz[int(test[-1].strip())][ocena] += 1
        acc = (macierz[0][0] + macierz[1][1]) / len(daneTestowe)
        p = macierz[0][0] / (macierz[0][0] + macierz[0][1])
        r = macierz[0][0] / (macierz[0][0] + macierz[1][0])
        f_miara = (2 * p * r) / (p + r)
        self.parent.showdata(f"Skuteczność wynosi {round(acc * 100, 2)}%\nF_miara {round(f_miara, 4)} \n",
                             important=False)
        self.parent.drawtable(dane=macierz, legenda="Oczekiwane\Wybrane", nazwa=f"Macierz omyłek:")

    def show_data(self):
        print(self.wordsDict)
