from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


class initial_parameters_and_funcrions():
    def __init__(self):
        self.p10 = 784800  # 100м
        self.g = 9.81
        self.c = 1000
        self.o = 0.01
        self.p20 = 156960  # 20 м
        self.w0 = 3000
        # Перевод в систему си
        self.o = self.o / 1000
        self.t = 0

    def find_lyam(self, Re, eps, d):
        if Re < 2320:
            lyam1 = 68 / Re
        elif (10 * eps) > Re >= 2320:
            lyam1 = 0.3164 / Re ** 0.25
        elif (10 * eps) <= Re < (500 * d / self.o):
            lyam1 = 0.11 * (eps + 68 / Re) ** 0.25
        else:
            lyam1 = 0.11 * (eps) ** 0.25
        return (lyam1)



class Window_Canvas(QMainWindow):
    def __init__(self, p0, V0, H0, xx, p_ism, V_ism, H_ism, t_rab, T, num_of_elements_in_lists):
        super().__init__()
        self.p0 = p0
        self.V0 = V0
        self.H0 = H0
        self.H_ism = H_ism
        self.p_ism = p_ism
        self.V_ism = V_ism
        self.T = T
        self.t_rab = t_rab
        self.xx = xx
        self.num_of_elements_in_lists = num_of_elements_in_lists
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        canvas = FigureCanvas(Figure(figsize=(10, 10)))
        layout.addWidget(canvas)
        self.ax1 = canvas.figure.add_subplot(4, 1, 2)
        self.ax2 = canvas.figure.add_subplot(4, 1, 3)
        self.ax3 = canvas.figure.add_subplot(4, 1, 1)
        self.ax4 = canvas.figure.add_subplot(4, 1, 4)
        self.ax1.set_xlabel('X, м')
        self.ax2.set_xlabel('X, м')
        self.ax3.set_xlabel('X, м')
        self.ax1.set_ylabel('P, Мпа')
        self.ax2.set_ylabel('V, м/с')
        self.ax3.set_ylabel('H, м')
        self.ax2.set_ylim(-5, 5)
        self.ax1.set_ylim(-3000000, 7000000)
        self.ax3.set_ylim(-500, 700)
        self.linep, = self.ax1.plot(xx, p0, c='green')
        self.lineV, = self.ax2.plot(xx, V0)
        self.lineH, = self.ax3.plot(xx, H0, c="red")
        self.ax4.plot(xx, vis_otm[0: self.num_of_elements_in_lists])

        self.Animate()

    def Animate(self):
        t = 0
        i = 0
        while t <= self.t_rab:
            self.ax3.set_title(f't = {round(t, 2)} ' + 'c')
            self.linep.set_ydata(self.p_ism[i])
            self.lineV.set_ydata(self.V_ism[i])
            self.lineH.set_ydata(self.H_ism[i])

            plt.gcf().canvas.flush_events()
            self.draw_ax(self.lineH)
            self.draw_ax(self.lineV)
            self.draw_ax(self.linep)
            time.sleep(0.01)
            t += self.T
            i += 1


    def draw_ax(self, line):
        line.figure.canvas.draw()


class Window(QMainWindow, initial_parameters_and_funcrions):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Mchar")
        self.setGeometry(450, 150, 1000, 750)
        """Начальные значения счетчика кликов"""
        self.n_btn_Pump = 0
        self.n_btn_Pipe = 0
        self.n_btn_Tap = 0
        """Основная строка трубопровода"""
        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Pipeline: ->")
        self.main_text.move(50, 75)
        self.main_text.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 19px;"
        )

        self.main_text.adjustSize()

        '''Ввод времени работы'''
        self.text_t_rab = QtWidgets.QLabel(self)
        self.text_t_rab.setText('Время расчета в сек: ')
        self.text_t_rab.move(50, 215)
        self.text_t_rab.setFixedSize(150, 25)
        self.text_t_rab.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        self.edit_t_rab = QtWidgets.QLineEdit(self)
        self.edit_t_rab.setText('1000')
        self.edit_t_rab.move(200, 215)
        self.edit_t_rab.setFixedSize(100, 25)
        self.edit_t_rab.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        self.edit_t_rab.setValidator(QtGui.QIntValidator(0, 9999))

        """Ввод плотности"""
        self.text_ro = QtWidgets.QLabel(self)
        self.text_ro.setText("Плотность в кг/м^3: ")
        self.text_ro.move(50, 250)
        self.text_ro.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        self.text_ro.setFixedSize(150, 25)

        self.edit_ro = QtWidgets.QLineEdit(self)
        self.edit_ro.setText('800')
        self.edit_ro.move(200, 250)
        self.edit_ro.setFixedSize(100, 25)
        self.edit_ro.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        self.edit_ro.setValidator(QtGui.QIntValidator(0, 9999))

        '''Ввод кинематич вязкости'''
        self.text_v = QtWidgets.QLabel(self)
        self.text_v.setText("Кин. вязкость в сСт: ")
        self.text_v.move(50, 285)
        self.text_v.setFixedSize(150, 25)
        self.text_v.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        self.edit_v = QtWidgets.QLineEdit(self)
        self.edit_v.setText('10')
        self.edit_v.move(200, 285)
        self.edit_v.setStyleSheet(
            "font-family: Monospac821 BC;"
            "font-size: 14px;"
        )
        self.edit_v.setFixedSize(100, 25)
        self.edit_v.setValidator(QtGui.QIntValidator(0, 9999))

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
        ''' Кнопка добавления крана'''
        self.btn_Tap = QtWidgets.QPushButton(self)
        self.btn_Tap.setText("Gate valve")
        self.btn_Tap.move(390, 450)
        self.btn_Tap.setFixedSize(120, 40)
        self.btn_Tap.setStyleSheet(
            "background-color: rgb(170, 85, 255);"
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
        self.btn_exit.clicked.connect(lambda: QtWidgets.qApp.quit())

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

        '''Списки параметров для объектов'''
        self.pipe_par = []
        self.pump_par = []
        self.tap_par = []
        self.main_text_backend = ['left_boundary']
        """Кнопки добавления объектов"""

    def clicked_btns_add(self):
        self.btn_Pipe.clicked.connect(lambda: self.add_smth('Pipe'))
        self.btn_Pump.clicked.connect(lambda: self.add_smth('Pump'))
        self.btn_Tap.clicked.connect(lambda: self.add_smth('Gate valve'))

    def add_smth(self, what_to_add):

        if what_to_add == self.btn_Pipe.text():
            self.pipe_par_moment = []

            def add_pipeline_len_In_pipe_par_window():
                self.pipe_par_moment.append(int(edit_L.text()))
                self.pipe_par_moment.append(int(edit_d.text()) / 1000)
                self.pipe_par.append(self.pipe_par_moment)
                self.main_text.setText(
                    self.main_text.text() + what_to_add + '(' + edit_L.text() + 'км' + ', ' + edit_d.text() + 'мм)' + "->")
                self.main_text_backend.append(what_to_add)
                self.n_btn_Pipe += 1
                pipe_par_window.close()

            pipe_par_window = QDialog()
            pipe_par_window.setWindowTitle("Выбор параметров трубопровода")
            pipe_par_window.setFixedSize(210, 150)
            lbl_L = QtWidgets.QLabel(pipe_par_window)
            lbl_L.setText('Укажите длину трубопровода в км:')
            lbl_L.move(10, 10)
            edit_L = QtWidgets.QLineEdit(pipe_par_window)
            edit_L.setText("100")
            edit_L.move(10, 30)
            edit_L.setValidator(QtGui.QIntValidator(0, 999))
            lbl_d = QtWidgets.QLabel(pipe_par_window)
            lbl_d.setText("Укажите диаметр трубопровода в мм: ")
            lbl_d.move(10, 60)
            edit_d = QtWidgets.QLineEdit(pipe_par_window)
            edit_d.setText('1000')
            edit_d.move(10, 80)
            edit_d.setValidator(QtGui.QIntValidator(0, 1999))
            btn_ok = QtWidgets.QPushButton(pipe_par_window)
            btn_ok.setText('Ok')
            btn_ok.move(100, 120)
            btn_ok.clicked.connect(add_pipeline_len_In_pipe_par_window)
            pipe_par_window.exec_()


        elif what_to_add == self.btn_Pump.text():
            self.pump_par_moment = []

            def add_pump_par():
                self.pump_par_moment.append(float(edit_a.text()))
                self.pump_par_moment.append(float(edit_b.text()))
                if rad_vkl_p.isChecked():
                    self.pump_par_moment.append(1)
                elif rad_vikl_p.isChecked():
                    self.pump_par_moment.append(2)
                else:
                    self.pump_par_moment.append(0)
                self.pump_par_moment.append(int(edit_time_p.text()))
                self.pump_par_moment.append(int(edit_t_vkl.text()))
                self.pump_par.append(self.pump_par_moment)
                self.main_text.setText(self.main_text.text() + what_to_add + "->")
                self.main_text_backend.append(what_to_add)
                self.n_btn_Pump += 1
                pump_par_window.close()

            pump_par_window = QDialog()
            pump_par_window.setWindowTitle("Выбор параметров насоса")
            pump_par_window.setFixedSize(200, 330)
            lbl_a = QtWidgets.QLabel(pump_par_window)
            lbl_a.move(10, 10)
            lbl_a.setText("Укажите параметр а:")
            lbl_a.adjustSize()
            edit_a = QtWidgets.QLineEdit(pump_par_window)
            edit_a.move(10, 30)
            edit_a.setText("310")
            edit_a.setValidator(QtGui.QIntValidator(0, 9999))
            lbl_b = QtWidgets.QLabel(pump_par_window)
            lbl_b.move(10, 60)
            lbl_b.setText("Укажите параметр b:")
            edit_b = QtWidgets.QLineEdit(pump_par_window)
            edit_b.move(10, 80)
            edit_b.setText("0.0000008")
            # edit_b.setValidator(QtGui.QDoubleValidator(0, 999999, 10))
            lbl_char_p = QtWidgets.QLabel(pump_par_window)
            lbl_char_p.setText("Выберите характер работы насоса:")
            lbl_char_p.move(10, 110)
            gr_box = QtWidgets.QGroupBox(pump_par_window)
            gr_box.move(10, 130)
            hlayout_for_radio_buttons = QtWidgets.QHBoxLayout(gr_box)
            rad_vkl_p = QtWidgets.QRadioButton()
            rad_vkl_p.setText("Вкл")
            rad_vkl_p.isChecked()
            rad_vikl_p = QtWidgets.QRadioButton()
            rad_vikl_p.setText("Выкл")
            hlayout_for_radio_buttons.addWidget(rad_vkl_p)
            hlayout_for_radio_buttons.addWidget(rad_vikl_p)
            lbl_time_p = QtWidgets.QLabel(pump_par_window)
            lbl_time_p.setText("Укажите время вкл/выкл в сек:")
            lbl_time_p.move(10, 180)
            edit_time_p = QtWidgets.QLineEdit(pump_par_window)
            edit_time_p.move(10, 200)
            edit_time_p.setText("0")
            edit_time_p.setValidator(QtGui.QIntValidator(0, 9999))
            lbl_t_vkl = QtWidgets.QLabel(pump_par_window)
            lbl_t_vkl.setText("Укажите время выбега насоса в сек: ")
            lbl_t_vkl.move(10, 230)
            edit_t_vkl = QtWidgets.QLineEdit(pump_par_window)
            edit_t_vkl.setText("20")
            edit_t_vkl.move(10, 250)
            edit_t_vkl.setValidator(QtGui.QIntValidator(0, 99))

            btn_ok_pump = QtWidgets.QPushButton(pump_par_window)
            btn_ok_pump.setText("Ok")
            btn_ok_pump.move(100, 290)
            btn_ok_pump.clicked.connect(add_pump_par)
            pump_par_window.exec_()


        elif what_to_add == self.btn_Tap.text():
            self.tap_par_moment = []

            def add_tap_par():
                if rad_vkl.isChecked():
                    self.tap_par_moment.append(1)
                elif rad_vikl.isChecked():
                    self.tap_par_moment.append(2)
                else:
                    self.tap_par_moment.append(3)
                self.tap_par_moment.append(int(edit_time_t.text()))
                self.tap_par_moment.append(int(edit_t_otkr.text()))
                self.tap_par_moment.append(int(edit_procent.text()))
                self.main_text.setText(self.main_text.text() + what_to_add + "->")
                self.main_text_backend.append(what_to_add)
                self.tap_par.append(self.tap_par_moment)
                self.n_btn_Tap += 1
                tap_par_window.close()

            tap_par_window = QDialog()
            tap_par_window.setWindowTitle("Выбор параметров крана")
            tap_par_window.setFixedSize(220, 270)
            lbl_char = QtWidgets.QLabel(tap_par_window)
            lbl_char.setText("Выберите характер работы крана:")
            lbl_char.move(10, 10)
            gr_box = QtWidgets.QGroupBox(tap_par_window)
            gr_box.move(10, 30)
            hlayout_for_radio_buttons = QtWidgets.QHBoxLayout(gr_box)
            rad_vkl = QtWidgets.QRadioButton()
            rad_vkl.setText("Открытие")
            rad_vkl.isChecked()
            rad_vikl = QtWidgets.QRadioButton()
            rad_vikl.setText("Закрытие")
            hlayout_for_radio_buttons.addWidget(rad_vkl)
            hlayout_for_radio_buttons.addWidget(rad_vikl)
            lbl_time_t = QtWidgets.QLabel(tap_par_window)
            lbl_time_t.setText("Укажите время начала откр/закр в сек:")
            lbl_time_t.move(10, 80)
            edit_time_t = QtWidgets.QLineEdit(tap_par_window)
            edit_time_t.move(10, 100)
            edit_time_t.setText("100")
            edit_time_t.setValidator(QtGui.QIntValidator(0, 9999))
            lbl_t_otkr = QtWidgets.QLabel(tap_par_window)
            lbl_t_otkr.setText("Укажите время откр/закр в сек:")
            lbl_t_otkr.move(10, 130)
            edit_t_otkr = QtWidgets.QLineEdit(tap_par_window)
            edit_t_otkr.setText('100')
            edit_t_otkr.move(10, 150)
            edit_t_otkr.setValidator(QtGui.QIntValidator(0, 999))
            lbl_procent = QtWidgets.QLabel(tap_par_window)
            lbl_procent.setText("Укажите процент откр/закр крана: ")
            lbl_procent.move(10, 180)
            edit_procent = QtWidgets.QLineEdit(tap_par_window)
            edit_procent.setText("100")
            edit_procent.move(10, 200)
            edit_procent.setValidator(QtGui.QIntValidator(0, 99))
            btn_ok_tap = QtWidgets.QPushButton(tap_par_window)
            btn_ok_tap.setText('Ok')
            btn_ok_tap.move(115, 245)
            btn_ok_tap.clicked.connect(add_tap_par)
            tap_par_window.exec_()

        self.main_text.adjustSize()

    '''Кнопки управления'''

    def clicked_btn_reset(self):
        self.btn_reset.clicked.connect(lambda: self.reset())

    def reset(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def clicked_btn_start(self):
        self.btn_start.clicked.connect(lambda: self.start())

        """Основная функция"""

    def start(self):
        self.ro = int(self.edit_ro.text())
        self.t_rab = int(self.edit_t_rab.text())
        self.v = int(self.edit_v.text()) / 1000000

        '''Чтение высотных отметок'''
        with open("Example.txt") as text_z:
            vis_otm_str = text_z.read().split(',')
            global vis_otm
            vis_otm = []
            for x in vis_otm_str:
                x = int(x)
                vis_otm.append(x)
            text_z.close()

        def find_Jb(Davleniya, Skorosty, d, i):
            Vjb = Skorosty
            Re = abs(Vjb) * d / self.v
            lyamjb = self.find_lyam(Re, self.o / d, d)
            Jb = Davleniya - self.ro * self.c * Skorosty + lyamjb * self.ro * Skorosty * abs(
                Skorosty) * T * self.c / (2 * d) + T * self.ro * self.c * self.g * (vis_otm[i + 1] - vis_otm[i]) / 1000
            return (Jb)

        def find_Ja(Davleniya, Skorosty, d, i):
            Vja = Skorosty
            Re = abs(Vja) * d / self.v
            lyamja = self.find_lyam(Re, self.o / d, d)
            Ja = Davleniya + self.ro * self.c * Skorosty - lyamja * self.ro * Skorosty * abs(
                Skorosty) * T * self.c / (2 * d) - T * self.ro * self.c * self.g * (vis_otm[i] - vis_otm[i - 1]) / 1000
            return (Ja)

        def count_H(p, i, V):
            H = p / (self.ro * self.g) + vis_otm[i] + (V ** 2) / (2 * self.g)
            return H

        def pump_method(P, V, i, a, b, char, chto_vivodim, d, t_vkl, t_char):
            ''' char( 0 - насоса всегда работает, 1 - насос вкл на tt секунде, 2 - насос выкл на tt сек, другое - выключен)'''

            if char == 0:
                w = self.w0
            elif char == 1:  # Включение на tt сек
                if t_char <= self.t <= t_char + t_vkl:
                    w = self.w0 / t_vkl * (self.t - t_char)
                elif self.t < t_char:
                    w = 0
                else:
                    w = self.w0
            elif char == 2:  # Выключение на ttt сек
                if self.t < t_char:
                    w = self.w0
                elif t_char <= self.t <= (t_char + t_vkl):
                    w = self.w0 - self.w0 / t_vkl * (self.t - t_char)
                else:
                    w = 0
            else:
                w = 0

            a = (w / self.w0) ** 2 * a  # 302.06   Характеристика насоса # b = 8 * 10 ** (-7)
            S = np.pi * (d / 2) ** 2
            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d, i)
            Jb = find_Jb(P[-1][i + 2], V[-1][i + 2], d, i)
            VV = (-self.c / self.g + (
                    (self.c / self.g) ** 2 - b * (S * 3600) ** 2 * ((Jb - Ja) / (self.ro * self.g) - a)) ** 0.5) / (
                         b * (S * 3600) ** 2)
            p1 = (Ja - self.ro * self.c * VV)
            p2 = (Jb + self.ro * self.c * VV)
            H1 = count_H(p1, i, VV)
            H2 = count_H(p2, i, VV)

            if chto_vivodim == 1:
                return [p1, VV, H1]
            else:
                return [p2, VV, H2]

        def pipe_method(P, V, i, d):
            """Условие, может быть, нужно будет переписать"""
            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d, i)
            Jb = find_Jb(P[-1][i + 1], V[-1][i + 1], d, i)
            pp = (Ja + Jb) / (2)
            VV = (Ja - Jb) / (2 * self.ro * self.c)
            H = count_H(pp, i, VV)
            return [pp, VV, H]

        def tap_method(P, V, i, chto_vivodim, char, t_char, d, t_otkr, procent):
            ''' char( 0 - кран всегда открыт, 1 - кран открывается на tt секунде, 2 - кран закр на tt сек, другое - закрыт)'''

            # угол открытия крана(стр 446, Идельчик)

            def find_zet(nu):
                if 0 <= nu < 10:
                    zet = (0.32 / 10) * nu + 0.04
                elif 10 <= nu < 20:
                    zet = (1.6 - 0.36) / 10 * (nu - 10) + 0.36
                elif 20 <= nu < 30:
                    zet = (5 - 1.6) / 10 * (nu - 20) + 1.6
                elif 30 <= nu < 40:
                    zet = (15 - 5) / 10 * (nu - 30) + 5
                elif 40 <= nu < 50:
                    zet = (42.5 - 15) / 10 * (nu - 40) + 15
                elif 50 <= nu < 60:
                    zet = (130 - 42.5) / 10 * (nu - 50) + 42.5
                elif 60 <= nu < 70:
                    zet = (800 - 130) / 10 * (nu - 60) + 130
                elif 70 <= nu < 80:
                    zet = (2500 - 800) / 10 * (nu - 70) + 800
                elif 80 <= nu < 85:
                    zet = (6000 - 2500) / 10 * (nu - 80) + 2500
                else:  # 85 <= nu <= 100:
                    zet = (100000000 - 6000) / 15 * (nu - 85) + 6000
                return zet

            if char == 0:
                nu = 0
                zet = find_zet(nu)
            elif char == 1:  # открытие на tt сек
                if t_char <= self.t <= t_char + t_otkr:
                    nu = 100 - procent / t_otkr * (self.t - t_char)
                    zet = find_zet(nu)
                elif self.t < t_char:
                    nu = 100
                    zet = find_zet(nu)
                else:
                    nu = (100 - procent)
                    zet = find_zet(nu)
            elif char == 2:  # закрытие на ttt сек
                if self.t < t_char:
                    nu = 0
                    zet = find_zet(nu)
                elif t_char <= self.t <= (t_char + t_otkr):
                    nu = procent / t_otkr * (self.t - t_char)
                    zet = find_zet(nu)
                else:
                    nu = procent
                    zet = find_zet(nu)
            else:
                nu = 100
                zet = find_zet(nu)

            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d, i)
            Jb = find_Jb(P[-1][i + 2], V[-1][i + 2], d, i)
            VV = (-2 * self.c * self.ro + (4 * self.ro ** 2 * self.c ** 2 - 2 * zet * self.ro * (Jb - Ja)) ** 0.5) / (
                    zet * self.ro)
            #VV = (Ja - Jb)/(self.ro * self.c) * (1 + (zet/(2*self.ro * (self.c)**2) * (Ja - Jb))**0.5)**(-1)
            p1 = (Ja - self.ro * self.c * VV)
            p2 = (Jb + self.ro * self.c * VV)
            H1 = count_H(p1, i, VV)
            H2 = count_H(p2, i, VV)
            if chto_vivodim == 1:
                return [p1, VV, H1]
            else:
                return [p2, VV, H2]

        def right_boundary_method(P, V, i, p_const, d):

            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d, i)
            VV = (Ja - p_const) / (self.ro * self.c)
            pp = p_const
            H = count_H(p_const, i, VV)
            return [pp, VV, H]

        def left_boundary_method(P, V, i, p_const, d):
            Jb = find_Jb(P[-1][i + 1], V[-1][i + 1], d, i)
            VV = (p_const - Jb) / (self.ro * self.c)
            pp = p_const
            H = count_H(p_const, i, VV)
            return [pp, VV, H]

        def Animation(p0, V0, H0, xx, p_ism, V_ism, H_ism):
            '''не смог разобраться в модуле анимации библиотеки матплотлиб, поэтому написал свой
             тоже не очень важно
            тут p_ism и v_ism это вложенный двухуровневый список, т.е. список внутри списка'''
            plt.ion()
            plt.style.use('seaborn-whitegrid')
            fig = plt.figure(figsize=(10, 10))
            ax1 = fig.add_subplot(4, 1, 2)
            ax2 = fig.add_subplot(4, 1, 3)
            ax3 = fig.add_subplot(4, 1, 1)
            ax4 = fig.add_subplot(4, 1, 4)
            ax1.set_xlabel('X, м')
            ax2.set_xlabel('X, м')
            ax3.set_xlabel('X, м')
            ax1.set_ylabel('P, Мпа')
            ax2.set_ylabel('V, м/с')
            ax3.set_ylabel('H, м')
            ax2.set_ylim(-5, 5)
            ax1.set_ylim(-3000000, 7000000)
            ax3.set_ylim(-500, 700)
            ax4.set_xlabel('X, м')
            ax4.set_ylabel('z, м')
            linep, = ax1.plot(xx, p0, c='green')
            lineV, = ax2.plot(xx, V0)
            lineH, = ax3.plot(xx, H0, c="red")
            ax4.plot(xx, vis_otm[0: num_of_elements_in_lists])
            t = 0
            i = 0
            while t <= self.t_rab:
                ax3.set_title(f't = {round(t, 2)} ' + 'c')
                linep.set_ydata(p_ism[i])
                linep.set_xdata(xx)
                lineV.set_ydata(V_ism[i])
                lineV.set_xdata(xx)
                lineH.set_ydata(H_ism[i])
                lineH.set_xdata(xx)
                plt.draw()
                plt.gcf().canvas.flush_events()
                time.sleep(0.01)
                t += T
                i += 1
            plt.ion()
            plt.show()

        '''Определение количества элементов в списках'''
        L = 0
        N = 0
        num_of_elements_in_lists = 0

        for i in range(len(self.pipe_par)):
            num_of_elements_in_lists += self.pipe_par[i][0]
            L += self.pipe_par[i][0] * 1000
            N += self.pipe_par[i][0]
        num_of_elements_in_lists += self.n_btn_Pump * 2 + 2 + self.n_btn_Tap * 2
        L += 2000
        N += 3
        '''Задание общих параметров трубопровода'''

        T = L / (N * self.c)
        """Начальные списки соростей и давлений на основе количества кликов"""
        P_O = [0.1] * num_of_elements_in_lists
        V_O = P_O
        H_O = P_O
        Davleniya = [P_O]
        Skorosty = [V_O]
        Napory = [H_O]
        self.pipe_par.append([100, 1])  # чтобы избежать ошибок, когда кран в конце
        '''Инициализация объектов и расчет'''
        self.main_text_backend.append('right_boundary')
        while self.t <= self.t_rab:
            count_pump_iter = 0
            iter = 0
            main = []
            count_pipe_iter = 0
            count_tap_iter = 0
            for i, x in enumerate(self.main_text_backend):
                if x == 'Pump':
                    main.append(pump_method(Davleniya, Skorosty, iter, self.pump_par[count_pump_iter][0],
                                            self.pump_par[count_pump_iter][1],
                                            self.pump_par[count_pump_iter][2],
                                            1, self.pipe_par[count_pipe_iter][1], self.pump_par[count_pump_iter][4],
                                            self.pump_par[count_pump_iter][3]))
                    main.append(pump_method(Davleniya, Skorosty, iter, self.pump_par[count_pump_iter][0],
                                            self.pump_par[count_pump_iter][1],
                                            self.pump_par[count_pump_iter][2],
                                            2, self.pipe_par[count_pipe_iter][1], self.pump_par[count_pump_iter][4],
                                            self.pump_par[count_pump_iter][3]))
                    count_pump_iter += 1
                    iter += 2
                elif x == 'Pipe':
                    for j in range(self.pipe_par[count_pipe_iter][0]):
                        main.append(pipe_method(Davleniya, Skorosty, iter, self.pipe_par[count_pipe_iter][1]))
                        iter += 1
                    count_pipe_iter += 1
                elif x == 'Gate valve':
                    main.append(tap_method(Davleniya, Skorosty, iter, 1, self.tap_par[count_tap_iter][0],
                                           self.tap_par[count_tap_iter][1], self.pipe_par[count_pipe_iter][1],
                                           self.tap_par[count_tap_iter][2], self.tap_par[count_tap_iter][3]))
                    main.append(tap_method(Davleniya, Skorosty, iter, 2, self.tap_par[count_tap_iter][0],
                                           self.tap_par[count_tap_iter][1], self.pipe_par[count_pipe_iter][1],
                                           self.tap_par[count_tap_iter][2], self.tap_par[count_tap_iter][3]))
                    iter += 2
                    count_tap_iter += 1
                elif x == 'right_boundary':
                    main.append(right_boundary_method(Davleniya, Skorosty, iter, self.p20,
                                                      self.pipe_par[count_pipe_iter - 1][1]))
                    iter += 1
                elif x == 'left_boundary':
                    main.append(
                        left_boundary_method(Davleniya, Skorosty, iter, self.p10, self.pipe_par[count_pipe_iter][1]))
                    iter += 1
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
            # По напору
            H_moment = []
            for i in range(len(main)):
                H_moment.append(main[i][2])
            Napory.append(H_moment)
        '''Создание списка координат'''
        dx = L / N
        x = 0
        xx = []
        count_pipe_iter = 0
        for i, y in enumerate(self.main_text_backend):
            if y == 'Pump':
                xx.extend([x, x])
                x += dx
            elif y == 'Pipe':
                for j in range((self.pipe_par[count_pipe_iter][0])):
                    xx.append(x)
                    x += dx
                count_pipe_iter += 1
            elif y == 'Gate valve':
                xx.extend([x, x])
                x += dx
            elif y == 'right_boundary' or 'left_boundary':
                xx.append(x)
                x += dx

        Animation(Davleniya[0], Skorosty[0], Napory[0], xx, Davleniya, Skorosty, Napory)
        # w = Window_Canvas(Davleniya[0], Skorosty[0], Napory[0], xx, Davleniya, Skorosty, Napory, self.t_rab, T, num_of_elements_in_lists).show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())

'''чтение файла высотных отметок и преобразование в целочисленный список'''
# with open('Example.txt', 'w+') as text:
#     for i in range(10000):
#         text.write(str(random.randint(0, 200))+',')
