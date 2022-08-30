from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QDialog

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import matplotlib.pyplot as plt
import numpy as np
import sys


class initial_parameters_and_funcrions():
    def __init__(self):
        self.p10 = 0.784800  # 100м
        self.g = 9.81
        self.c = 1000

        # self.d = 1000
        self.o = 0.01
        self.p20 = 0.15696  # 20 м
        self.ro = 800
        self.v = 10
        self.t_rab = 1000  # Время работы
        self.w0 = 3000
        # Перевод в систему си
        # self.d = self.d / 1000
        self.o = self.o / 1000
        self.v = self.v / 1000000
        self.t = 0
        # self.T = self.L / (self.N * self.c)

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
        self.btn_Tap.setText("Tap")
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

        '''Списки параметров для объектов'''
        self.pipe_par = []
        self.pump_par = []
        self.tap_par = []
        self.main_text_backend = []
        """Кнопки добавления объектов"""

    def clicked_btns_add(self):
        self.btn_Pipe.clicked.connect(lambda: self.add_smth('Pipe'))
        self.btn_Pump.clicked.connect(lambda: self.add_smth('Pump'))
        self.btn_Tap.clicked.connect(lambda: self.add_smth('Tap'))

    def add_smth(self, what_to_add):

        if what_to_add == self.btn_Pipe.text():
            self.pipe_par_moment = []

            def add_pipeline_len_In_pipe_par_window():
                self.pipe_par_moment.append(int(edit_L.text()))
                self.pipe_par_moment.append(int(edit_d.text()) / 1000)
                self.pipe_par.append(self.pipe_par_moment)
                self.main_text.setText(self.main_text.text() + what_to_add + "->")
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
            lbl_d = QtWidgets.QLabel(pipe_par_window)
            lbl_d.setText("Укажите диаметр трубопровода в мм: ")
            lbl_d.move(10, 60)
            edit_d = QtWidgets.QLineEdit(pipe_par_window)
            edit_d.setText('1000')
            edit_d.move(10, 80)
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
                self.pump_par.append(self.pump_par_moment)
                self.main_text.setText(self.main_text.text() + what_to_add + "->")
                self.main_text_backend.append(what_to_add)
                self.n_btn_Pump += 1
                pump_par_window.close()

            pump_par_window = QDialog()
            pump_par_window.setWindowTitle("Выбор параметров насоса")
            pump_par_window.setFixedSize(200, 270)
            lbl_a = QtWidgets.QLabel(pump_par_window)
            lbl_a.move(10, 10)
            lbl_a.setText("Укажите параметр а:")
            lbl_a.adjustSize()
            edit_a = QtWidgets.QLineEdit(pump_par_window)
            edit_a.move(10, 30)
            edit_a.setText("310")
            lbl_b = QtWidgets.QLabel(pump_par_window)
            lbl_b.move(10, 60)
            lbl_b.setText("Укажите параметр b:")
            edit_b = QtWidgets.QLineEdit(pump_par_window)
            edit_b.move(10, 80)
            edit_b.setText("0.0000008")
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
            btn_ok_pump = QtWidgets.QPushButton(pump_par_window)
            # btn_ok_pump.setFixedSize()
            btn_ok_pump.setText("Ok")
            btn_ok_pump.move(100, 230)
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
                    self.tap_par_moment.append(0)
                self.tap_par_moment.append(int(edit_time_t.text()))
                self.main_text.setText(self.main_text.text() + what_to_add + "->")
                self.main_text_backend.append(what_to_add)
                self.tap_par.append(self.tap_par_moment)
                self.n_btn_Tap += 1
                tap_par_window.close()
            tap_par_window = QDialog()
            tap_par_window.setWindowTitle("Выбор параметров крана")
            tap_par_window.setFixedSize(210, 150)
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
            lbl_time_t.setText("Укажите время откр/закр в сек:")
            lbl_time_t.move(10, 80)
            edit_time_t = QtWidgets.QLineEdit(tap_par_window)
            edit_time_t.move(10, 100)
            edit_time_t.setText("100")
            btn_ok_tap = QtWidgets.QPushButton(tap_par_window)
            btn_ok_tap.setText('Ok')
            btn_ok_tap.move(115, 125)
            btn_ok_tap.clicked.connect(add_tap_par)
            tap_par_window.exec_()

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

        def find_Jb(Davleniya, Skorosty, d):
            Vjb = Skorosty
            Re = abs(Vjb) * d / self.v
            lyamjb = self.find_lyam(Re, self.o / d, d)
            Jb = Davleniya * 1000000 - self.ro * self.c * Skorosty + lyamjb * self.ro * Skorosty * abs(
                Skorosty) * T * self.c / (2 * d)
            return (Jb)

        def find_Ja(Davleniya, Skorosty, d):
            Vja = Skorosty
            Re = abs(Vja) * d / self.v
            lyamja = self.find_lyam(Re, self.o / d, d)
            Ja = Davleniya * 1000000 + self.ro * self.c * Skorosty - lyamja * self.ro * Skorosty * abs(
                Skorosty) * T * self.c / (2 * d)
            return (Ja)

        def pump_method(P, V, i, a, b, number, char, chto_vivodim, d, t_char=0):
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
            S = np.pi * (d / 2) ** 2
            if number == 0:
                Ja = find_Ja(self.p10, 2, d)
            else:
                Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d)
            Jb = find_Jb(P[-1][i + 2], V[-1][i + 2], d)
            VV = (-self.c / self.g + (
                    (self.c / self.g) ** 2 - b * (S * 3600) ** 2 * ((Jb - Ja) / (self.ro * self.g) - a)) ** 0.5) / (
                         b * (S * 3600) ** 2)
            p1 = (Ja - self.ro * self.c * VV) / 1000000
            p2 = (Jb + self.ro * self.c * VV) / 1000000
            if chto_vivodim == 1:
                return [p1, VV]
            else:
                return [p2, VV]

        def pipe_method(P, V, i, d):

            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d)
            Jb = find_Jb(P[-1][i + 1], V[-1][i + 1], d)
            pp = (Ja + Jb) / (2 * 1000000)
            VV = (Ja - Jb) / (2 * self.ro * self.c)
            return [pp, VV]

        def tap_method(P, V, i, chto_vivodim, char, t_char, d):
            ''' char( 0 - кран всегда открыт, 1 - кран открывается на tt секунде, 2 - кран закр на tt сек, другое - закрыт)'''

            # угол открытия крана(стр 446, Идельчик)

            def find_zet(nu):
                if 0 <= nu < 10:
                    zet = (0.32 / 10) * nu + 0.04
                elif 10 <= nu < 20:
                    zet = (1.6 - 0.36) / 10 * nu + 0.36
                elif 20 <= nu < 30:
                    zet = (5 - 1.6) / 10 * nu + 1.6
                elif 30 <= nu < 40:
                    zet = (15 - 5) / 10 * nu + 5
                elif 40 <= nu < 50:
                    zet = (42.5 - 15) / 10 * nu + 15
                elif 50 <= nu < 60:
                    zet = (130 - 42.5) / 10 * nu + 42.5
                elif 60 <= nu < 70:
                    zet = (800 - 130) / 10 * nu + 130
                elif 70 <= nu < 80:
                    zet = (2500 - 800) / 10 * nu + 800
                elif 80 <= nu < 85:
                    zet = (6000 - 2500) / 10 * nu + 2500
                else:  # 85 <= nu <= 100:
                    zet = (1000000 - 6000) / 15 + 6000
                return zet

            if char == 0:
                nu = 0
                zet = find_zet(nu)
            elif char == 1:  # открытие на tt сек
                if t_char <= self.t <= t_char + 100:
                    nu = 1 * (self.t - t_char)
                    zet = find_zet(nu)
                elif self.t < t_char:
                    nu = 100
                    zet = find_zet(nu)
                else:
                    nu = 0
                    zet = find_zet(nu)
            elif char == 2:  # закрытие на ttt сек
                if self.t < t_char:
                    nu = 0
                    zet = find_zet(nu)
                elif t_char <= self.t <= (t_char + 100):
                    nu = 100 - 1 * (self.t - t_char)
                    zet = find_zet(nu)
                else:
                    nu = 100
                    zet = find_zet(nu)
            else:
                nu = 100
                zet = find_zet(nu)

            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d)
            Jb = find_Jb(P[-1][i + 2], V[-1][i + 2], d)
            VV = (-2 * self.c * self.ro + (4 * self.ro ** 2 * self.c ** 2 - 2 * zet * self.ro * (Jb - Ja)) ** 0.5) / (
                    zet * self.ro)
            p1 = (Ja - self.ro * self.c * VV) / 1000000
            p2 = (Jb + self.ro * self.c * VV) / 1000000
            if chto_vivodim == 1:
                return [p1, VV]
            else:
                return [p2, VV]

        def right_boundary_method(P, V, i, p_const, d):

            Ja = find_Ja(P[-1][i - 1], V[-1][i - 1], d)
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
                time.sleep(0.1)
                t += T
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
        num_of_elements_in_lists += self.n_btn_Pump * 2 + 1 + self.n_btn_Tap * 2
        L += 1000
        N += 2
        '''Задание общих параметров трубопровода'''

        T = L / (N * self.c)
        """Начальные списки соростей и давлений на основе количества кликов"""
        P_O = [0.1] * num_of_elements_in_lists
        V_O = P_O
        Davleniya = [P_O]
        Skorosty = [V_O]

        '''Инициализация объектов и расчет'''
        self.main_text_backend.append('')
        while self.t <= self.t_rab:
            count_pump_iter = 0
            iter = 0
            main = []
            count_pipe_iter = 0
            count_tap_iter = 0
            for i, x in enumerate(self.main_text_backend):
                if x == 'Pump':
                    main.append(pump_method(Davleniya, Skorosty, iter, self.pump_par[count_pump_iter][0],
                                            self.pump_par[count_pump_iter][1], count_pump_iter, self.pump_par[count_pump_iter][2],
                                            1, self.pipe_par[count_pipe_iter][1], self.pump_par[count_pump_iter][3]))
                    main.append(pump_method(Davleniya, Skorosty, iter, self.pump_par[count_pump_iter][0],
                                            self.pump_par[count_pump_iter][1], count_pump_iter, self.pump_par[count_pump_iter][2],
                                            2, self.pipe_par[count_pipe_iter][1], self.pump_par[count_pump_iter][3]))
                    count_pump_iter += 1
                    iter += 2
                elif x == 'Pipe':
                    for j in range(self.pipe_par[count_pipe_iter][0]):
                        main.append(pipe_method(Davleniya, Skorosty, iter, self.pipe_par[count_pipe_iter][1]))
                        iter += 1
                    count_pipe_iter += 1
                elif x == 'Tap':
                    main.append(tap_method(Davleniya, Skorosty, iter, 1, self.tap_par[count_tap_iter][0], self.tap_par[count_tap_iter][1], self.pipe_par[count_pipe_iter][1]))
                    main.append(tap_method(Davleniya, Skorosty, iter, 2, self.tap_par[count_tap_iter][0], self.tap_par[count_tap_iter][1], self.pipe_par[count_pipe_iter][1]))
                    iter += 2
                    count_tap_iter+=1
                elif x == '':
                    main.append(right_boundary_method(Davleniya, Skorosty, iter, self.p20,
                                                      self.pipe_par[count_pipe_iter - 1][1]))

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
            elif y == 'Tap':
                xx.extend([x, x])
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
