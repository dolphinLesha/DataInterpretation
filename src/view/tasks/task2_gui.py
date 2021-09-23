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
                             QFrame, QSizePolicy, QLineEdit, QGroupBox)

from src.control.function import *
from src.data.graphic import *
from src.data.tasks.default_values import DefaultTask2
from src.view.own_widgets import *


class WidgetPlotDrawRandom(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.init_style_sheet()

    def init_ui(self):
        vbox = SelfVLayout()
        self.setLayout(vbox)
        title = QLabel("Построение случайных функций")
        title.setFixedHeight(30)
        widget = QWidget()
        vbox.addWidget(title)
        vbox.addWidget(widget)
        self.main_h_box = SelfHLayout(spacing=10)
        widget.setLayout(self.main_h_box)
        self.view_graphics = WidgetPlots()
        self.view_control = WidgetControl()
        self.view_control.setFixedWidth(200)
        self.view_control.graph_build_b.clicked.connect(self.test)
        self.main_h_box.addWidget(self.view_control)
        self.main_h_box.addWidget(self.view_graphics)

    def init_style_sheet(self):
        # self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
        #         background-color:rgba(255,255,255,255)''')
        self.view_control.setStyleSheet('''QWidget{background-color: rgb(150,150,150);}''')

    def test(self):
        sender = self.sender()
        n = self.view_control.parameter_n_input.get_value_as_int()
        if n is None:
            n = DefaultTask2.n
        min_p = self.view_control.parameter_min_input.get_value_as_int()
        if min_p is None:
            min_p = DefaultTask2.min_p
        max_p = self.view_control.parameter_max_input.get_value_as_int()
        if max_p is None:
            max_p = DefaultTask2.max_p
        print(min_p)
        print(max_p)
        func = RandomFunc()
        func.build(n, min_p, max_p)
        Graphic(self.view_graphics.plots["plot1"]).build(func=func, prefab=GraphicPrefab.prefab_simple_thin())

        n = self.view_control.parameter_n_input2.get_value_as_int()
        if n is None:
            n = DefaultTask2.n
        min_p = self.view_control.parameter_min_input2.get_value_as_int()
        if min_p is None:
            min_p = DefaultTask2.min_p
        max_p = self.view_control.parameter_max_input2.get_value_as_int()
        if max_p is None:
            max_p = DefaultTask2.max_p
        precision = self.view_control.parameter_precision_input2.get_value_as_int()
        if precision is None:
            precision = DefaultTask2.precision
        func = RandomOwnFunc()
        func.build(n, min_p, max_p, precision=10 ** precision)
        Graphic(self.view_graphics.plots["plot2"]).build(func=func, prefab=GraphicPrefab.prefab_simple_thin())


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
        self.graph_build_b = SelfButton("построить графики")

        '''group box for values of 1 graph'''
        group1 = QGroupBox("Параметры 1 графика")
        box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(box_group1)
        self.parameter_n_input = SelfTitledLineEdit(title="Value N", hint_text="500")
        self.parameter_min_input = SelfTitledLineEdit(title="Value Min", hint_text="-1")
        self.parameter_max_input = SelfTitledLineEdit(title="Value Max", hint_text="1")
        box_group1.addWidget(self.parameter_n_input)
        box_group1.addWidget(self.parameter_min_input)
        box_group1.addWidget(self.parameter_max_input)

        '''group box for values of 2 graph'''
        group2 = QGroupBox("Параметры 2 графика")
        box_group2 = SelfVLayout(spacing=5)
        group2.setLayout(box_group2)
        self.parameter_n_input2 = SelfTitledLineEdit(title="Value N", hint_text="500")
        self.parameter_min_input2 = SelfTitledLineEdit(title="Value Min", hint_text="-1")
        self.parameter_max_input2 = SelfTitledLineEdit(title="Value Max", hint_text="1")
        self.parameter_precision_input2 = SelfTitledLineEdit(title="Value Precision", hint_text="5")
        box_group2.addWidget(self.parameter_n_input2)
        box_group2.addWidget(self.parameter_min_input2)
        box_group2.addWidget(self.parameter_max_input2)
        box_group2.addWidget(self.parameter_precision_input2)

        self.box.addWidget(self.graph_build_b)
        self.box.addWidget(group1)
        self.box.addWidget(group2)
        self.box.addStretch(1)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#z2wid{background-color: rgb(150,150,150);}''')
        pass


class WidgetPlots(QWidget):
    def __init__(self, size: QSize = None):
        super().__init__()
        if size is not None:
            self.setFixedSize(size)
        self.init_ui()

    def init_ui(self):
        self.setObjectName("plots")
        self.vbox = SelfVLayout()
        self.setLayout(self.vbox)
        self.hbox1 = SelfHLayout()
        self.hbox2 = SelfHLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.plots = {}
        self.l_u_plot = self.build_plot_item(frame_name='left_up_plot', plot_name='plot1', plot_title='первый график')
        self.r_u_plot = self.build_plot_item(frame_name='right_up_plot', plot_name='plot2', plot_title='второй график')
        self.hbox1.addWidget(self.l_u_plot)
        self.hbox1.addWidget(self.r_u_plot)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#plots{background-color: rgba(240,240,240,255); padding: 0px;}''')

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
