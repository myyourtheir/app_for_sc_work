from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import time
import matplotlib.pyplot as plt
import numpy as np
import sys


class initial_parameters_and_funcrions():
    def __init__(self):
        self.p10 = 0.784800  # 100м
        self.g = 9.81
        self.c = 1000

        self.d = 1000
        self.o = 0.01
        self.p20 = 0.15696  # 20 м
        self.ro = 800
        self.v = 10
        self.t_rab = 1000  # Время, когда вкл насос
        self.w0 = 3000
        self.n = 2  # кол-во участков
        self.N = 100 * self.n + 1  # Количество сечений
        self.L = 100 * self.n + 1  # 1 - краевое условие

        # Перевод в систему си
        self.L = self.L * 1000
        self.d = self.d / 1000
        self.o = self.o / 1000
        self.p10 = self.p10 * 1000000
        self.p20 = self.p20 * 1000000
        self.v = self.v / 1000000
        self.t = 0
        self.T = self.L / (self.N * self.c)

    def find_lyam(self, Re, eps):
        if Re < 2320:
            lyam1 = 68 / Re
        elif (10 * eps) > Re >= 2320:
            lyam1 = 0.3164 / Re ** 0.25
        elif (10 * eps) <= Re < (500 * self.d / self.o):
            lyam1 = 0.11 * (eps + 68 / Re) ** 0.25
        else:
            lyam1 = 0.11 * (eps) ** 0.25
        return (lyam1)

    def find_Jb(self, Davleniya, Skorosty):
        Vjb = Skorosty
        Re = abs(Vjb) * self.d / self.v
        lyamjb = self.find_lyam(Re, self.o / self.d)
        Jb = Davleniya * 1000000 - self.ro * self.c * Skorosty + lyamjb * self.ro * Skorosty * abs(
            Skorosty) * self.T * self.c / (2 * self.d)
        return (Jb)

    def find_Ja(self, Davleniya, Skorosty):
        Vja = Skorosty
        Re = abs(Vja) * self.d / self.v
        lyamja = self.find_lyam(Re, self.o / self.d)
        Ja = Davleniya * 1000000 + self.ro * self.c * Skorosty - lyamja * self.ro * Skorosty * abs(
            Skorosty) * self.T * self.c / (2 * self.d)
        return (Ja)


class Window(QMainWindow, initial_parameters_and_funcrions):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Mchar")
        self.setGeometry(450, 150, 1000, 750)
        """Начальные значения счетчика кликов"""
        self.n_btn_Pump = 0
        self.n_btn_Pipe = 0

        """Основная строка трубопровода"""
        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Pipeline: ")
        self.main_text.move(50, 75)
        self.main_text.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 19px;"
        )
        self.main_text.adjustSize()

        """Кнопка добавления насоса"""
        self.btn_Pump = QtWidgets.QPushButton(self)
        self.btn_Pump.setText("Pump")
        self.btn_Pump.move(50, 450)
        self.btn_Pump.setFixedSize(120, 40)
        self.btn_Pump.setStyleSheet(
            "background-color: rgb(0, 85, 255);"
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )

        '''Кнопка добавления трубы'''
        self.btn_Pipe = QtWidgets.QPushButton(self)
        self.btn_Pipe.setText("Pipe")
        self.btn_Pipe.move(220, 450)
        self.btn_Pipe.setFixedSize(120, 40)
        self.btn_Pipe.setStyleSheet(
            "background-color: rgb(85, 255, 127);"
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )

        '''Кнопка старт'''
        self.btn_start = QtWidgets.QPushButton(self)
        self.btn_start.setText("Start")
        self.btn_start.move(440, 660)
        self.btn_start.setFixedSize(120, 40)
        self.btn_start.setStyleSheet(
            "background-color: rgb(255, 6, 81);"
            "font-family: Monospac821 BC;"
            "font-size: 20px;"
        )

        """Кнопка выхода"""
        self.btn_exit = QtWidgets.QPushButton(self)
        self.btn_exit.setText("Exit")
        self.btn_exit.move(900, 700)
        self.btn_exit.setFixedSize(80, 20)
        self.btn_exit.setStyleSheet(
            "background-color: rgb(176, 176, 176);"
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        # btn_exit.clicked.connect(app.exec_())

        """Кнопка обновления строки"""
        self.btn_reset = QtWidgets.QPushButton(self)
        self.btn_reset.setText("Reset")
        self.btn_reset.move(800, 150)
        self.btn_reset.setStyleSheet(
            "background-color: rgb(176, 176, 176);"
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        """действия кнопок"""
        self.clicked_btns_add()
        self.clicked_btn_reset()
        """Кнопки добавления объектов"""

    def clicked_btns_add(self):
        self.btn_Pipe.clicked.connect(lambda: self.add_smth(self.btn_Pipe.text()))
        self.btn_Pump.clicked.connect(lambda: self.add_smth(self.btn_Pump.text()))

    def add_smth(self, what_to_add):
        self.main_text.setText(self.main_text.text() + what_to_add + "->")
        if what_to_add == self.btn_Pipe.text():
            self.n_btn_Pipe += 1
        elif what_to_add == self.btn_Pump.text():
            self.n_btn_Pump += 1
        self.main_text.adjustSize()

    def clicked_btn_reset(self):
        self.btn_reset.clicked.connect(lambda: self.reset())

    def reset(self):
        self.main_text.setText("Pipeline: ")
        self.n_btn_Pump = 0
        self.n_btn_Pipe = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())
