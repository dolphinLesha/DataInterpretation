from PyQt5 import QtWidgets, QtCore
import sys
import datetime
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize, QRect, QThread, pyqtSignal
import pyqtgraph as pg
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
from src.data.graphic import Graphic


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
        self.l_u_plot = self.left_up()
        self.r_u_plot = self.right_up()
        self.r_d_plot = self.right_down()
        self.l_d_plot = self.left_down()
        self.hbox1.addWidget(self.l_u_plot)
        self.hbox1.addWidget(self.r_u_plot)
        self.hbox2.addWidget(self.r_d_plot)
        self.hbox2.addWidget(self.l_d_plot)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.main_frame.setStyleSheet('''QWidget#plots{background-color: rgba(240,240,240,255); padding: 0px;}''')
        self.plot1.setStyleSheet('''QWidget#plot{background-color: rgba(240,240,210,255);}''')
        pass

    def left_up(self) -> QWidget:
        main_frame = QFrame()
        main_frame.setObjectName("left_up_plot")
        vbox = QVBoxLayout(main_frame)
        self.plot1 = QLabel()
        self.plot1.setObjectName("plot")
        title = QLabel("Первый график")
        vbox.addWidget(self.plot1, stretch=9)
        vbox.addWidget(title, stretch=1)
        return main_frame

    def right_up(self) -> QWidget:
        main_frame = QFrame()
        main_frame.setObjectName("right_up_plot")
        vbox = QVBoxLayout(main_frame)
        self.plot2 = QLabel()
        self.plot2.setObjectName("plot")
        title = QLabel("Второй график")
        vbox.addWidget(self.plot2, stretch=9)
        vbox.addWidget(title, stretch=1)
        return main_frame

    def right_down(self) -> QWidget:
        main_frame = QFrame()
        main_frame.setObjectName("right_down_plot")
        vbox = QVBoxLayout(main_frame)
        self.plot3 = QLabel()
        self.plot3.setObjectName("plot")
        title = QLabel("Третий график")
        vbox.addWidget(self.plot3, stretch=9)
        vbox.addWidget(title, stretch=1)
        return main_frame

    def left_down(self) -> QWidget:
        main_frame = QFrame()
        main_frame.setObjectName("left_down_plot")
        vbox = QVBoxLayout(main_frame)
        self.plot4 = QLabel()
        self.plot4.setObjectName("plot")
        title = QLabel("Четвертый график")
        vbox.addWidget(self.plot4, stretch=9)
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
        fig = TrendExpFunc()
        fig.build(n, a, b)
        graph = Graphic(fig)
        height, width, channel = graph.data.shape
        bytesPerLine = 3 * width
        qImg = QImage(graph.data.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.view_graphics.plot1.setPixmap(
            QPixmap(qImg).scaled(self.view_graphics.plot1.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation))

        a, b, n = -0.1, 5, 500
        fig = TrendExpFunc()
        fig.build(n, a, b)
        graph = Graphic(fig)
        height, width, channel = graph.data.shape
        bytesPerLine = 3 * width
        qImg = QImage(graph.data.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.view_graphics.plot2.setPixmap(
            QPixmap(qImg).scaled(self.view_graphics.plot2.size(), QtCore.Qt.IgnoreAspectRatio,
                                 QtCore.Qt.SmoothTransformation))

        a, b, n = 5, 1, 500
        fig = TrendLinFunc()
        fig.build(n, a, b)
        graph = Graphic(fig)
        height, width, channel = graph.data.shape
        bytesPerLine = 3 * width
        qImg = QImage(graph.data.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.view_graphics.plot3.setPixmap(
            QPixmap(qImg).scaled(self.view_graphics.plot3.size(), QtCore.Qt.IgnoreAspectRatio,
                                 QtCore.Qt.SmoothTransformation))

        a, b, n = -10, 10, 500
        fig = TrendLinFunc()
        fig.build(n, a, b)
        graph = Graphic(fig)
        height, width, channel = graph.data.shape
        bytesPerLine = 3 * width
        qImg = QImage(graph.data.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.view_graphics.plot4.setPixmap(
            QPixmap(qImg).scaled(self.view_graphics.plot4.size(), QtCore.Qt.IgnoreAspectRatio,
                                 QtCore.Qt.SmoothTransformation))


app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
application = MainWindow()
application.show()

app.exec()
