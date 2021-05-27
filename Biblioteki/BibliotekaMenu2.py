from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QTableWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QInputDialog
import matplotlib.pyplot as plt


class MenuInterface:
    def collectdata(self, inputname, message) -> tuple:
        pass

    def askquestion(self, inputname, message) -> bool:
        pass

    def showdata(self, outputdata, important=False):
        pass

    def changeinfo(self, newtext):
        pass

    def drawplot(self, dane, nazwa="Wykres", osx="X", osy="Y"):
        pass

    def drawtable(self, dane, legenda="Brak legendy", nazwa="Tabelka", prefixx="", prefixy=""):
        pass

    def clear(self):
        pass


class ButtonMenu(QWidget, MenuInterface):

    def __init__(self, parent=None, name="Okienko", initinfo=""):
        super().__init__(parent)

        self.functions = dict()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.name = name

        self.resize(400, 100)
        self.setWindowTitle(self.name)

        self.infolabel = QLabel(initinfo, self)
        self.outputlabel = QLabel("", self)
        self.layout.addWidget(self.infolabel, 0, 0)
        self.layout.addWidget(self.outputlabel, 1, 0)

        self.tabelka = None
        self.tabelkalabel = None

        self.show()

    def collectdata(self, inputname, message):
        text, ok = QInputDialog.getText(self, inputname, message)
        return text, not ok

    def askquestion(self, inputname, message):
        qm = QMessageBox
        ret = qm.question(self, inputname, message, qm.Yes | qm.No)
        return ret == qm.Yes

    def showdata(self, outputdata, important=False):
        if important:
            msgBox = QMessageBox()
            msgBox.setText(outputdata)
            msgBox.exec_()
        else:
            self.outputlabel.setText(outputdata)

    def addbutton(self, name, function):
        self.functions[name] = function
        button = QPushButton(name)
        self.layout.addWidget(button, len(self.functions.keys()) + 1, 0)
        button.clicked.connect(function)
        self.repaint()

    def changeinfo(self, newtext):
        self.infolabel.setText(newtext)
        self.infolabel.repaint()

    def drawplot(self, dane, nazwa="Wykres", osx="X", osy="Y"):
        if isinstance(dane, dict):
            plt.plot(dane.keys(), dane.values())

        plt.title(nazwa)
        plt.xlabel(osx, fontsize=14)
        plt.ylabel(osy, fontsize=14)
        plt.show()

    def drawtable(self, dane: dict, legenda="Brak legendy", nazwa="Tabelka", prefixx="", prefixy=""):

        self.tabelkalabel = QLabel(nazwa)
        self.layout.addWidget(self.tabelkalabel, 19, 0)

        self.tabelka = QTableWidget()
        self.tabelka.setRowCount(len(dane) + 1)
        self.tabelka.setColumnCount(len(dane) + 1)
        for i, el in enumerate(dane):
            self.tabelka.setItem(i + 1, 0, QTableWidgetItem(prefixx + str(el)))
            self.tabelka.setItem(0, i + 1, QTableWidgetItem(prefixy + str(el)))
        for j, slownik in enumerate(dane.items()):
            for z, wynik in enumerate(slownik[1].items()):
                self.tabelka.setItem(1 + j, 1 + z, QTableWidgetItem(str(wynik[1])))
        self.tabelka.setItem(0, 0, QTableWidgetItem(legenda))

        self.layout.addWidget(self.tabelka, 20, 0)

    def clear(self):
        self.tabelka.setVisible(False)
        self.tabelkalabel.setVisible(False)
