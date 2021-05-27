import sys
from Biblioteki import ButtonMenu
from PyQt5.QtWidgets import QApplication
from Core import Core

app = QApplication(sys.argv)

okno = ButtonMenu(name="Perceptron by s21001")
rdzen = Core(okno, trainFilePath="data.csv", wordsDictPath="word_list.txt")

okno.addbutton("Wypisz Dane", rdzen.show_data)
okno.addbutton("Ocen zdanie", rdzen.ocen)
okno.addbutton("Policz skuteczność", rdzen.skutecznosc)
okno.addbutton("Podziel zbiór danych", rdzen.podziel_dane)
app.exec_()



