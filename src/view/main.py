import time

from PyQt5 import QtWidgets, QtCore
import sys
import datetime
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize, QRect, QThread, pyqtSignal
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import (QGridLayout,
                             QPushButton,
                             QLabel,
                             QWidget,
                             QScrollArea,
                             QInputDialog,
                             QLineEdit,
                             QFileDialog,
                             QVBoxLayout,
                             QHBoxLayout,
                             QTextEdit,
                             QMessageBox,
                             QFrame,
                             QProgressBar,
                             QScrollBar)

from src.control.function import *
from src.data.graphic import *


class WidgetControl(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self.setFixedSize(size)
        self.init_ui()

    def init_ui(self):
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("control_main_frame")
        self.main_frame.setFixedSize(self.size())
        self.box = QVBoxLayout(self.main_frame)
        self.graph_build_b = QPushButton("построить графики")
        self.parameter_a_input = QTextEdit()
        # self.parameter_a_input.setInputMethodHints(Qt_InputMethodHint)
        self.box.addWidget(self.graph_build_b)
        self.box.addStretch(1)
        self.init_style_sheet()

    def init_style_sheet(self):
        # self.main_frame.setStyleSheet('''QWidget#control_main_frame{background-color: rgba(0,255,255,255);}''')
        # self.button.setStyleSheet('''QWidget{background-color: rgba(0,0,255,255);}''')
        # self.her.setStyleSheet('''QWidget{background-color: rgba(0,0,255,255);}''')
        pass


class WidgetPlots(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self.setFixedSize(size)
        self.init_ui()

    def init_ui(self):
        self.main_frame = QFrame(self)
        print(self.size())
        self.main_frame.setFixedSize(self.size())
        self.main_frame.setObjectName("plots")
        self.vbox = QVBoxLayout(self)
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.plots = {}
        self.l_u_plot = self.build_plot_item(frame_name='left_up_plot', plot_name='plot1', plot_title='первый график')
        self.r_u_plot = self.build_plot_item(frame_name='right_up_plot', plot_name='plot2', plot_title='второй график')
        self.r_d_plot = self.build_plot_item(frame_name='right_down_plot', plot_name='plot3', plot_title='четвертый график')
        self.l_d_plot = self.build_plot_item(frame_name='left_down_plot', plot_name='plot4', plot_title='третий график')
        self.hbox1.addWidget(self.l_u_plot)
        self.hbox1.addWidget(self.r_u_plot)
        self.hbox2.addWidget(self.r_d_plot)
        self.hbox2.addWidget(self.l_d_plot)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.main_frame.setStyleSheet('''QWidget#plots{background-color: rgba(240,240,240,255); padding: 0px;}''')
        # self.plot1.setStyleSheet('''QWidget#plot{background-color: rgba(240,240,210,255);}''')
        pass

    def build_plot_item(self, **kwargs) -> QWidget:
        main_frame = QFrame()
        main_frame.setObjectName(kwargs['frame_name'])
        vbox = QVBoxLayout(main_frame)
        self.plots[kwargs['plot_name']] = pg.PlotWidget()
        self.plots[kwargs['plot_name']].setBackground('w')
        self.plots[kwargs['plot_name']].setObjectName(kwargs['plot_name'])
        title = QLabel(kwargs['plot_title'])
        vbox.addWidget(self.plots[kwargs['plot_name']], stretch=9)
        vbox.addWidget(title, stretch=1)
        return main_frame


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(str(datetime.datetime.now()))
        self.init_ui()
        self.init_style_sheet()
        # self.test()

    def init_ui(self):
        self.setFixedWidth(1280)
        self.setFixedHeight(720)
        print(self.size())

        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("main_main_frame")
        self.main_frame.setGeometry(0, 0, self.width(), self.height())
        self.main_h_box = QHBoxLayout(self.main_frame)
        self.view_graphics = WidgetPlots(QSize(self.width() / 5 * 4 - 20, self.height() - 20))
        self.view_control = WidgetControl(QSize(self.width() / 5 * 1 - 20, self.height() - 20))
        self.view_control.graph_build_b.clicked.connect(self.test)
        self.main_h_box.addWidget(self.view_control, stretch=1)
        self.main_h_box.addWidget(self.view_graphics, stretch=4)
        print(self.view_graphics.size())

    def init_style_sheet(self):
        self.main_frame.setStyleSheet('''QWidget#main_main_frame{
                background-color:rgba(220,220,220,255)}''')
        self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
        background-color:rgba(255,255,255,255)''')
        self.setStyleSheet('''QWidget#plot{background-color: rgba(0,255,255,255);}''')

    def test(self):
        sender = self.sender()

        a, b, n = 0.4, 1, 500
        func = TrendExpFunc()
        func.build(n, a, b)
        Graphic(self.view_graphics.plots["plot1"]).build(func=func, prefab=GraphicPrefab.prefab_simple())

        a, b, n = -0.1, 5, 500
        func = TrendExpFunc()
        func.build(n, a, b)
        Graphic(self.view_graphics.plots["plot2"]).build(func=func, prefab=GraphicPrefab.prefab_simple())

        a, b, n = 5, 1, 500
        func = TrendLinFunc()
        func.build(n, a, b)
        Graphic(self.view_graphics.plots["plot3"]).build(func=func, prefab=GraphicPrefab.prefab_simple())

        a, b, n = -10, 10, 500
        func = TrendLinFunc()
        func.build(n, a, b)
        Graphic(self.view_graphics.plots["plot4"]).build(func=func, prefab=GraphicPrefab.prefab_simple())


app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
application = MainWindow()
application.show()

app.exec()
