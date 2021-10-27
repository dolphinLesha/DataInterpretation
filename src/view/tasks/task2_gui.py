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
from src.view.view_settings import ViewSettings


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
        self.view_control.setFixedWidth(ViewSettings.control_width)
        self.view_control.graph_build_b.clicked.connect(self.test)
        self.main_h_box.addWidget(self.view_control)
        self.main_h_box.addWidget(self.view_graphics)

    def init_style_sheet(self):
        # self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
        #         background-color:rgba(255,255,255,255)''')
        self.view_control.setStyleSheet('''QWidget{background-color: rgb(150,150,150);}''')

    def test(self):
        sender = self.sender()

        func1 = self.view_control.graph_and_settings1.get_function()
        func1.build(**self.view_control.graph_and_settings1.get_settings())
        Graphic(self.view_graphics.plots["plot1"]).build(func=func1, prefab=GraphicPrefab.prefab_simple_thin())

        func2 = self.view_control.graph_and_settings2.get_function()
        func2.build(**self.view_control.graph_and_settings2.get_settings())
        Graphic(self.view_graphics.plots["plot2"]).build(func=func2, prefab=GraphicPrefab.prefab_simple_thin())

        func3 = AddFunction()
        func3.build(**{'funcs': [func1, func2]})
        Graphic(self.view_graphics.plots["plot3"]).build(func=func3, prefab=GraphicPrefab.prefab_simple_thin())

        func4 = MultiplyFunction()
        func4.build(**{'funcs': [func1, func2]})
        Graphic(self.view_graphics.plots["plot4"]).build(func=func4, prefab=GraphicPrefab.prefab_simple_thin())


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
        group1 = QGroupBox("график рандома")
        box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(box_group1)
        self.graph_and_settings1 = SelfFuncSettingsWidget()
        box_group1.addWidget(self.graph_and_settings1)

        '''group box for values of 2 graph'''
        group2 = QGroupBox("график для наложения")
        box_group2 = SelfVLayout(spacing=5)
        group2.setLayout(box_group2)
        self.graph_and_settings2 = SelfFuncSettingsWidget()
        box_group2.addWidget(self.graph_and_settings2)

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
        self.l_d_plot = self.build_plot_item(frame_name='left_down_plot', plot_name='plot3', plot_title='+ график')
        self.r_d_plot = self.build_plot_item(frame_name='right_down_plot', plot_name='plot4', plot_title='* график')
        self.hbox1.addWidget(self.l_u_plot)
        self.hbox1.addWidget(self.r_u_plot)
        self.hbox2.addWidget(self.l_d_plot)
        self.hbox2.addWidget(self.r_d_plot)

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
