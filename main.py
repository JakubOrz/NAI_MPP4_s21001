import sys
from Biblioteki import ButtonMenu
from PyQt5.QtWidgets import QApplication
from Core import Core

app = QApplication(sys.argv)

okno = ButtonMenu(name="Naiwny klasyfikator Bayesa s21001")
if len(sys.argv) >= 3:
    rdzen = Core(okno, trainFilePath=sys.argv[1], wordsDictPath=sys.argv[2])
    okno.addbutton("Wypisz Dane", rdzen.show_data)
    okno.addbutton("Ocen zdanie", rdzen.ocen)
    okno.addbutton("Policz skuteczność", rdzen.skutecznosc)
    okno.addbutton("Podziel zbiór danych", rdzen.podziel_dane)
    app.exec_()
else:
    print(f"Nie podano ścieżki do pliku z danymi treningowymi oraz word dict")
