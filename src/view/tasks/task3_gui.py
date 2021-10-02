import datetime
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QPushButton,
                             QLabel,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QTextEdit,
                             QFrame, QSizePolicy, QLineEdit, QGroupBox, QComboBox, QScrollArea)

from src.control.analysis import AnalysisBuilder
from src.control.function import *
from src.data.graphic import *
from src.data.tasks.default_values import DefaultTask2
from src.view.own_widgets import *


class WidgetStatistics(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.init_style_sheet()

    def init_ui(self):
        vbox = SelfVLayout()
        self.setLayout(vbox)
        title = QLabel("Статистические данные набора")
        title.setFixedHeight(30)
        widget = QWidget()
        vbox.addWidget(title)
        vbox.addWidget(widget)
        self.main_h_box = SelfHLayout(spacing=10)
        widget.setLayout(self.main_h_box)
        self.view_graphics = WidgetValues()
        self.view_control = WidgetControl()
        self.view_control.setFixedWidth(200)
        self.view_control.graph_build_b.clicked.connect(self.build_graph)
        self.view_control.stats_build_b.clicked.connect(self.build_stats)
        self.main_h_box.addWidget(self.view_control)
        self.main_h_box.addWidget(self.view_graphics)

    def init_style_sheet(self):
        # self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
        #         background-color:rgba(255,255,255,255)''')
        self.view_control.setStyleSheet('''QWidget{background-color: rgb(150,150,150);}''')

    def build_graph(self):
        sender = self.sender()

        self.func = self.view_control.graph_and_settings.get_function()
        self.func.build(**self.view_control.graph_and_settings.get_settings())
        Graphic(self.view_graphics.plots["plot1"]).build(func=self.func, prefab=GraphicPrefab.prefab_simple_thin())
        self.view_control.stats_build_b.setEnabled(True)

    def build_stats(self):
        sender = self.sender()


        stats = AnalysisBuilder(self.func)
        stats.build_values()
        m = DefaultTask3.m
        if mm := self.view_control.parameter_m_input.get_value_as_int():
            m = mm
        e = DefaultTask3.e
        if ee := self.view_control.parameter_e_input.get_value_as_int():
            e = ee
        stat_answer = stats.check_stac(m, e)
        self.view_graphics.min_value_t.set_text(str(stats.min))
        self.view_graphics.max_value_t.set_text(str(stats.max))
        self.view_graphics.mo_value_t.set_text(str(stats.average))
        self.view_graphics.D_value_t.set_text(str(stats.var))
        self.view_graphics.co_value_t.set_text(str(stats.std))
        self.view_graphics.ck_value_t.set_text(str(stats.ms))
        self.view_graphics.cko_value_t.set_text(str(stats.rms))
        self.view_graphics.A_value_t.set_text(str(stats.asymmetry))
        self.view_graphics.aC_value_t.set_text(str(stats.asymmetry_coefficient))
        self.view_graphics.E_value_t.set_text(str(stats.excess))
        self.view_graphics.eC_value_t.set_text(str(stats.kurtosis))


        self.view_graphics.mo_widget.setParent(None)
        self.view_graphics.D_widget.setParent(None)
        self.view_graphics.mo_widget.destroy()
        self.view_graphics.D_widget.destroy()

        self.view_graphics.mo_widget = QWidget()
        self.view_graphics.D_widget = QWidget()
        self.view_graphics.mo_scroll.setWidget(self.view_graphics.mo_widget)
        self.view_graphics.D_scroll.setWidget(self.view_graphics.D_widget)

        self.view_graphics.mo_lay = SelfVLayout()
        self.view_graphics.D_lay = SelfVLayout()
        self.view_graphics.mo_widget.setLayout(self.view_graphics.mo_lay)
        self.view_graphics.D_widget.setLayout(self.view_graphics.D_lay)

        for i in range(stats.stat_mo.__len__()):
            lab = QLabel(str(i*m) + '-' + str(i*m+m) + ": " + str(stats.stat_mo[i]))
            lab.setFixedHeight(20)
            self.view_graphics.mo_lay.addWidget(lab)
            lab2 = QLabel(str(i*m) + '-' + str(i*m+m) + ": " + str(stats.stat_D[i]))
            lab2.setFixedHeight(20)
            self.view_graphics.D_lay.addWidget(lab2)
        self.view_graphics.mo_lay.addStretch()
        self.view_graphics.D_lay.addStretch()
        self.view_graphics.stat_answer.set_text("Процесс стационарный" if stat_answer else "Процесс не стационарный")



class WidgetControl(QWidget):
    def __init__(self, size: QSize = None):
        super().__init__()
        if size is not None:
            self.setFixedSize(size)
        self.setObjectName("z2wid")
        self.init_ui()
        self.init_style_sheet()

    def init_ui(self):
        self.box = SelfVLayout(spacing=15)
        self.setLayout(self.box)
        self.graph_build_b = SelfButton("Построить график")

        '''group box for values of 1 graph'''
        group1 = QGroupBox("Основной график")
        self.box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(self.box_group1)
        self.graph_and_settings = SelfFuncSettingsWidget()
        self.box_group1.addWidget(self.graph_and_settings)

        '''group box for values for 2 part of task'''
        group2 = QGroupBox("Настройки стационарности")
        self.box_group2 = SelfVLayout(spacing=5)
        group2.setLayout(self.box_group2)
        self.parameter_m_input = SelfTitledLineEdit("Кол-во элементов в разбиении", str(DefaultTask3.m))
        self.parameter_e_input = SelfTitledLineEdit("Предел в процентах", str(DefaultTask3.e))
        self.box_group2.addWidget(self.parameter_m_input)
        self.box_group2.addWidget(self.parameter_e_input)

        self.stats_build_b = SelfButton("Вычислить статистику")
        self.stats_build_b.setEnabled(False)
        self.box.addWidget(self.graph_build_b)
        self.box.addWidget(self.stats_build_b)
        self.box.addWidget(group1)
        self.box.addWidget(group2)
        self.box.addStretch(1)
        self.init_style_sheet()





    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#z2wid{background-color: rgb(150,150,150);}''')
        pass


class WidgetValues(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("values")
        self.hbox = SelfHLayout(spacing=10)
        self.setLayout(self.hbox)
        self.vbox1 = SelfVLayout()
        self.vbox2 = SelfVLayout(spacing=0)
        self.vbox3 = SelfVLayout()
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox3)
        self.min_value_t = SelfTitledLabel("Минимум", "", 200)
        self.max_value_t = SelfTitledLabel("Максимум", "", 200)
        self.mo_value_t = SelfTitledLabel("Мат. ожидание", "", 200)
        self.D_value_t = SelfTitledLabel("Дисперсия", "", 200)
        self.co_value_t = SelfTitledLabel("Стандартное отклонение", "", 200)
        self.ck_value_t = SelfTitledLabel("Средне квадратическое", "", 200)
        self.cko_value_t = SelfTitledLabel("Средне квадратическое отклонение", "", 250)
        self.A_value_t = SelfTitledLabel("Асимметрия", "", 200)
        self.aC_value_t = SelfTitledLabel("коэфициент асимметрии", "", 200)
        self.E_value_t = SelfTitledLabel("эксцесс", "", 200)
        self.eC_value_t = SelfTitledLabel("куртозис", "", 200)
        self.vbox2.addWidget(self.min_value_t)
        self.vbox2.addWidget(self.max_value_t)
        self.vbox2.addWidget(self.mo_value_t)
        self.vbox2.addWidget(self.D_value_t)
        self.vbox2.addWidget(self.co_value_t)
        self.vbox2.addWidget(self.ck_value_t)
        self.vbox2.addWidget(self.cko_value_t)
        self.vbox2.addWidget(self.A_value_t)
        self.vbox2.addWidget(self.aC_value_t)
        self.vbox2.addWidget(self.E_value_t)
        self.vbox2.addWidget(self.eC_value_t)
        self.vbox2.addStretch()
        self.mo_scroll = QScrollArea()
        self.D_scroll = QScrollArea()
        self.mo_scroll.setFixedHeight(500)
        self.D_scroll.setFixedHeight(500)

        hbox31 = SelfHLayout()
        self.vbox3.addLayout(hbox31)
        self.stat_answer = SelfTitledLabel("Призак стационарности")
        hbox31.addWidget(self.mo_scroll)
        hbox31.addWidget(self.D_scroll)
        self.vbox3.addWidget(self.stat_answer)
        self.mo_widget = QWidget()
        self.mo_lay = SelfVLayout(spacing=2)
        self.mo_widget.setLayout(self.mo_lay)
        self.D_widget = QWidget()
        self.D_lay = SelfVLayout(spacing=2)
        self.D_widget.setLayout(self.D_lay)
        self.mo_scroll.setWidget(self.mo_widget)
        self.mo_scroll.setWidgetResizable(True)
        self.D_scroll.setWidget(self.D_widget)
        self.D_scroll.setWidgetResizable(True)
        self.plots = {}
        self.plot = self.build_plot_item(plot_name='plot1', plot_title='График функции')
        self.plot.setFixedSize(400, 400)
        self.vbox1.addWidget(self.plot)
        self.vbox1.addStretch()
        self.vbox3.addStretch()

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#values{background-color: rgba(240,240,240,255); padding: 0px;}''')

    def build_plot_item(self, **kwargs) -> QWidget:
        widget = QWidget()
        vbox = SelfVLayout()
        widget.setLayout(vbox)
        self.plots[kwargs['plot_name']] = pg.PlotWidget()
        self.plots[kwargs['plot_name']].setBackground('w')
        self.plots[kwargs['plot_name']].setObjectName(kwargs['plot_name'])
        title = QLabel(kwargs['plot_title'])
        title.setFixedHeight(30)
        vbox.addWidget(self.plots[kwargs['plot_name']], stretch=9)
        vbox.addWidget(title, stretch=1)
        return widget
