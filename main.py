import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QTableWidget, QWidget, QLabel, QPushButton


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(768, 512)
        self.vl = QVBoxLayout(self)
        self.hl = QHBoxLayout(self)
        self.hl2 = QHBoxLayout(self)
        self.tableWidget = QTableWidget(self)
        self.label = QLabel(self)
        self.add_btn = QPushButton('добавить', self)
        self.change_btn = QPushButton('изменить', self)

        self.changeFlag = True

        self.con = sqlite3.connect("../capuchino/coffee.db")
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM info""").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))

        myl = ["ID", "Название", "Степень обжарки", "молотый/в зёрнах", "вкус", "цена", "объём"]

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setHorizontalHeaderItem(j, QTableWidgetItem(str(myl[j])))
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        self.add_btn.clicked.connect(self.add_item)
        self.change_btn.clicked.connect(self.change)

        self.vl.addWidget(self.tableWidget)
        self.vl.addWidget(self.add_btn)
        self.vl.addWidget(self.change_btn)

    def add_item(self):
        self.changeFlag = False
        self.do_it()

    def change(self):
        self.changeFlag = True
        self.do_it()

    def do_it(self):
        if self.changeFlag:
            kk = list(self.tableWidget.selectedIndexes())
            if kk:
                kk = list(self.tableWidget.selectedIndexes())[0].row() + 1
            else:
                kk = None
        else:
            kk = None
        self.adi = AddChangeItem(kk)
        self.adi.show()


class AddChangeItem(QWidget):
    def __init__(self, idid):
        super().__init__()
        self.id = idid
        print(self.id)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.btn_save.clicked.connect(self.save)
        self.btn_close.clicked.connect(self.close)

        self.change = False

        myl = ["ID", "Название", "Степень обжарки", "молотый/в зёрнах", "вкус", "цена", "объём"]
        self.con = sqlite3.connect("../capuchino/coffee.db")
        self.cur = self.con.cursor()

        if self.id:
            self.change = True
            result = self.cur.execute("""SELECT * FROM info
                                        WHERE id = ?""", (self.id, )).fetchall()

        else:
            self.change = False
            result = [('', '', '', '', '', '', '')]

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setHorizontalHeaderItem(j, QTableWidgetItem(str(myl[j])))
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def save(self):
        mm = []
        for i in range(self.tableWidget.columnCount()):
            mm.append(self.tableWidget.item(0, i).text())
        if self.change:
            self.cur.execute("""UPDATE info SET
                                            name = ?
                                            WHERE id = ?""", (mm[1], self.id, ))
            self.cur.execute("""UPDATE info SET
                                            degree = ?
                                            WHERE id = ?""", (mm[2], self.id, ))
            self.cur.execute("""UPDATE info SET
                                            type = ?
                                            WHERE id = ?""", (mm[3], self.id, ))
            self.cur.execute("""UPDATE info SET
                                            taste = ?
                                            WHERE id = ?""", (mm[4], self.id, ))
            self.cur.execute("""UPDATE info SET
                                            price = ?
                                            WHERE id = ?""", (mm[5], self.id, ))
            self.cur.execute("""UPDATE info SET
                                            size = ?
                                            WHERE id = ?""", (mm[6], self.id, ))
        else:
            print(mm)
            del mm[0]
            print(mm)
            self.cur.execute("""INSERT INTO info(name, degree, type, taste, price, size)
                            VALUES(?, ?, ?, ?, ?, ?)""", (mm[0], mm[1], mm[2], mm[3], mm[4], mm[5], ))
        self.con.commit()
        print(mm)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())
