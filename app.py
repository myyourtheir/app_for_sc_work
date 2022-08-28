from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        self.t_rab = 1000  # Время работы
        self.w0 = 3000
        # self.n = 2  # кол-во участков
        # self.N = 100 * self.n + 1  # Количество сечений
        # self.L = 100 * self.n + 1  # 1 - краевое условие

        # Перевод в систему си
        # self.L = self.L * 1000
        self.d = self.d / 1000
        self.o = self.o / 1000
        self.v = self.v / 1000000
        self.t = 0
        # self.T = self.L / (self.N * self.c)

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
        self.main_text.setText("Pipeline: ->")
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
        self.clicked_btn_start()
        """Кнопки добавления объектов"""

    def clicked_btns_add(self):
        self.btn_Pipe.clicked.connect(lambda: self.add_smth(self.btn_Pipe.text()))
        self.btn_Pump.clicked.connect(lambda: self.add_smth(self.btn_Pump.text()))

    def add_smth(self, what_to_add):
        self.main_text.setText(self.main_text.text() + what_to_add + "->")
        if what_to_add == self.btn_Pipe.text():
            pipe_par_window = QMessageBox()
            pipe_par_window.setWindowTitle("Параметры трубопровода")
            pipe_par_window.setGeometry(850, 525, 300, 200)
            pipe_par_window.setText('Укажите длину трубопровода')
            sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, pipe_par_window)


            pipe_par_window.exec_()
            self.n_btn_Pipe += 1
        elif what_to_add == self.btn_Pump.text():
            self.n_btn_Pump += 1
        self.main_text.adjustSize()
        '''Кнопки управления'''

    def clicked_btn_reset(self):
        self.btn_reset.clicked.connect(lambda: self.reset())

    def reset(self):
        self.main_text.setText("Pipeline: ->")
        self.n_btn_Pump = 0
        self.n_btn_Pipe = 0

    def clicked_btn_start(self):
        self.btn_start.clicked.connect(lambda: self.start())

        """Основная функция"""

    def start(self):

        def find_Jb(Davleniya, Skorosty):
            Vjb = Skorosty
            Re = abs(Vjb) * self.d / self.v
            lyamjb = self.find_lyam(Re, self.o / self.d)
            Jb = Davleniya * 1000000 - self.ro * self.c * Skorosty + lyamjb * self.ro * Skorosty * abs(
                Skorosty) * T * self.c / (2 * self.d)
            return (Jb)

        def find_Ja(Davleniya, Skorosty):
            Vja = Skorosty
            Re = abs(Vja) * self.d / self.v
            lyamja = self.find_lyam(Re, self.o / self.d)
            Ja = Davleniya * 1000000 + self.ro * self.c * Skorosty - lyamja * self.ro * Skorosty * abs(
                Skorosty) * T * self.c / (2 * self.d)
            return (Ja)

        def pump_method(P, V, i, a, b, number, char, chto_vivodim, t_char=0):
            ''' char( 0 - насоса всегда работает, 1 - насос вкл на tt секунде, 2 - насос выкл на tt сек, другое - выключен)'''

            if char == 0:
                w = self.w0
            elif char == 1:  # Включение на tt сек
                if t_char <= self.t <= t_char + 20:
                    w = 150 * (self.t - t_char)
                elif self.t < t_char:
                    w = 0
                else:
                    w = 3000
            elif char == 2:  # Выключение на ttt сек
                if self.t < t_char:
                    w = 3000
                elif t_char <= self.t <= (t_char + 20):
                    w = 3000 - 150 * (self.t - t_char)
                else:
                    w = 0
            else:
                w = 0

            a = (w / self.w0) ** 2 * a  # 302.06   Характеристика насоса # b = 8 * 10 ** (-7)
            S = np.pi * (self.d / 2) ** 2
            if number == 0:
                Ja = find_Ja(self.p10, 2)
            else:
                Ja = find_Ja(P[-1][i - 1], V[-1][i - 1])
            Jb = find_Jb(P[-1][i + 2], V[-1][i + 2])
            VV = (-self.c / self.g + (
                    (self.c / self.g) ** 2 - b * (S * 3600) ** 2 * ((Jb - Ja) / (self.ro * self.g) - a)) ** 0.5) / (
                         b * (S * 3600) ** 2)
            p1 = (Ja - self.ro * self.c * VV) / 1000000
            p2 = (Jb + self.ro * self.c * VV) / 1000000
            if chto_vivodim == 1:
                return [p1, VV]
            else:
                return [p2, VV]

        def pipe_method(P, V, i):

            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1])
            Jb = find_Jb(P[-1][i + 1], V[-1][i + 1])
            pp = (Ja + Jb) / (2 * 1000000)
            VV = (Ja - Jb) / (2 * self.ro * self.c)
            return [pp, VV]

        def right_boundary_method(P, V, i, p_const):

            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1])
            VV = (Ja - p_const) / (self.ro * self.c)
            pp = p_const / 1000000
            return [pp, VV]

        def Animation(p0, V0, xx, p_ism, V_ism):
            '''не смог разобраться в модуле анимации библиотеки матплотлиб, поэтому написал свой
             тоже не очень важно
            тут p_ism и v_ism это вложенный двухуровневый список, т.е. список внутри списка'''
            plt.ion()
            plt.style.use('seaborn-whitegrid')
            fig = plt.figure(figsize=(7, 6))
            ax1 = fig.add_subplot(2, 1, 1)
            ax2 = fig.add_subplot(2, 1, 2)
            ax1.set_xlabel('X, м')
            ax2.set_xlabel('X, м')
            ax1.set_ylabel('P, Мпа')
            ax2.set_ylabel('V, м/с')
            ax2.set_ylim(-5, 5)
            ax1.set_ylim(-3, 7)

            linep, = ax1.plot(xx, p0, c='green')
            lineV, = ax2.plot(xx, V0)
            t = 0
            for i in range(self.t_rab):
                ax1.set_title(f't = {round(t)} ' + 'c')
                linep.set_ydata(p_ism[i])
                linep.set_xdata(xx)
                lineV.set_ydata(V_ism[i])
                lineV.set_xdata(xx)
                plt.draw()
                plt.gcf().canvas.flush_events()
                time.sleep(0.01)
                t += T
            plt.ion()
            plt.show()

        '''Определение количества элементов в списках'''
        num_of_elements_in_lists = self.n_btn_Pump * 2 + self.n_btn_Pipe * 100 + 1

        '''Задание общих параметров трубопровода'''
        L = self.n_btn_Pipe * 100000 + 1000
        N = self.n_btn_Pipe * 100 + 2
        T = L / (N * self.c)
        """Начальные списки соростей и давлений на основе количества кликов"""
        P_O = [0.1] * num_of_elements_in_lists
        V_O = P_O
        Davleniya = [P_O]
        Skorosty = [V_O]
        str_of_main_in_list = self.main_text.text().split('->')
        '''Инициализация объектов и расчет'''
        for tr in range(self.t_rab):
            pump_number = 0
            iter = 0
            main = []
            for i, x in enumerate(str_of_main_in_list):
                if x == 'Pump':
                    main.append(pump_method(Davleniya, Skorosty, iter, 310, 8 * 10 ** (-7), pump_number, 1, 1, 1))
                    main.append(pump_method(Davleniya, Skorosty, iter, 310, 8 * 10 ** (-7), pump_number, 1, 2, 1))
                    pump_number += 1
                    iter += 2
                elif x == 'Pipe':
                    for j in range(100):
                        main.append(pipe_method(Davleniya, Skorosty, iter))
                        iter += 1
                elif x == '':
                    main.append(right_boundary_method(Davleniya, Skorosty, iter, self.p20))
            '''Распаковка main'''

            # По давлению
            p_moment = []
            for i in range(len(main)):
                p_moment.append(main[i][0])
            Davleniya.append(p_moment)

            # По скорости
            V_moment = []
            for i in range(len(main)):
                V_moment.append(main[i][1])
            Skorosty.append(V_moment)
            self.t += T

        '''Создание списка координат'''
        dx = L / N
        x = 0
        xx = []
        for i, y in enumerate(str_of_main_in_list):
            if y == 'Pump':
                xx.extend([x, x])
                x += dx
            elif y == 'Pipe':
                for j in range(100):
                    xx.append(x)
                    x += dx
            elif y == '':
                xx.append(x)
                x += dx

        Animation(Davleniya[0], Skorosty[0], xx, Davleniya, Skorosty)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())
