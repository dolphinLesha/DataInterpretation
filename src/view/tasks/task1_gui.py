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
                             QFrame, QSizePolicy)

from src.control.function import *
from src.data.graphic import *
from src.view.own_widgets import *
from src.view.view_settings import ViewSettings


class WidgetPlotDraw1(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.init_style_sheet()

    def init_ui(self):
        vbox = SelfVLayout()
        self.setLayout(vbox)
        title = QLabel("Построение 4 графиков")
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
        self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
                background-color:rgba(255,255,255,255)''')

    def test(self):
        sender = self.sender()

        func = self.view_control.graph_and_settings1.get_function()
        func.build(**self.view_control.graph_and_settings1.get_settings())
        Graphic(self.view_graphics.plots["plot1"]).build(func=func, prefab=GraphicPrefab.prefab_simple())

        func = self.view_control.graph_and_settings2.get_function()
        func.build(**self.view_control.graph_and_settings2.get_settings())
        Graphic(self.view_graphics.plots["plot2"]).build(func=func, prefab=GraphicPrefab.prefab_simple())

        func = self.view_control.graph_and_settings3.get_function()
        func.build(**self.view_control.graph_and_settings3.get_settings())
        Graphic(self.view_graphics.plots["plot3"]).build(func=func, prefab=GraphicPrefab.prefab_simple())

        func = self.view_control.graph_and_settings4.get_function()
        func.build(**self.view_control.graph_and_settings4.get_settings())
        Graphic(self.view_graphics.plots["plot4"]).build(func=func, prefab=GraphicPrefab.prefab_simple())


class WidgetControl(QWidget):
    def __init__(self, size: QSize = None):
        super().__init__()
        if size is not None:
            self.setFixedSize(size)
        self.init_ui()

    def init_ui(self):
        self.box = SelfVLayout()
        self.setLayout(self.box)
        self.graph_build_b = SelfButton("построить графики")
        self.box.addWidget(self.graph_build_b)

        '''group box for values of 1 graph'''
        group1 = QGroupBox("График 1")
        self.box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(self.box_group1)
        self.graph_and_settings1 = SelfFuncSettingsWidget()
        self.box_group1.addWidget(self.graph_and_settings1)
        self.box.addWidget(group1)

        '''group box for values of 1 graph'''
        group2 = QGroupBox("График 2")
        self.box_group2 = SelfVLayout(spacing=5)
        group2.setLayout(self.box_group2)
        self.graph_and_settings2 = SelfFuncSettingsWidget()
        self.box_group2.addWidget(self.graph_and_settings2)
        self.box.addWidget(group2)

        '''group box for values of 1 graph'''
        group3 = QGroupBox("График 3")
        self.box_group3 = SelfVLayout(spacing=5)
        group3.setLayout(self.box_group3)
        self.graph_and_settings3 = SelfFuncSettingsWidget()
        self.box_group3.addWidget(self.graph_and_settings3)
        self.box.addWidget(group3)

        '''group box for values of 1 graph'''
        group4 = QGroupBox("График 4")
        self.box_group4 = SelfVLayout(spacing=5)
        group4.setLayout(self.box_group4)
        self.graph_and_settings4 = SelfFuncSettingsWidget()
        self.box_group4.addWidget(self.graph_and_settings4)
        self.box.addWidget(group4)



        self.box.addStretch(1)
        self.init_style_sheet()

    def init_style_sheet(self):
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
        self.r_d_plot = self.build_plot_item(frame_name='right_down_plot', plot_name='plot4',
                                             plot_title='четвертый график')
        self.l_d_plot = self.build_plot_item(frame_name='left_down_plot', plot_name='plot3', plot_title='третий график')
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
        vbox.addWidget(self.plots[kwargs['plot_name']], stretch=9)
        vbox.addWidget(title, stretch=1)
        return widget