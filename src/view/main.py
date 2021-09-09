from PyQt5 import QtWidgets, QtCore
import sys
import datetime
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize, QRect, QThread, pyqtSignal
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


class WidgetControl(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("control_main_frame")
        self.main_frame.setFixedSize(self.size())
        self.button = QPushButton("построить график", self.main_frame)
        self.init_style_sheet()

    def init_style_sheet(self):
        # self.main_frame.setStyleSheet('''QWidget#control_main_frame{background-color: rgba(0,255,255,255);}''')
        pass


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(str(datetime.datetime.now()))
        self.init_ui()
        self.init_style_sheet()

    def init_ui(self):
        self.setFixedWidth(1280)
        self.setFixedHeight(720)

        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("main_main_frame")
        self.main_frame.setGeometry(0, 0, self.width(), self.height())
        self.view_graphics = QWidget()
        self.view_control = WidgetControl()
        self.main_h_box = QHBoxLayout(self.main_frame)
        self.main_h_box.addWidget(self.view_control, stretch=1)
        self.main_h_box.addWidget(self.view_graphics, stretch=4)


    def init_style_sheet(self):
        self.main_frame.setStyleSheet('''QWidget#main_main_frame{
                background-color:rgba(220,220,220,255)}''')
        self.view_graphics.setStyleSheet('''border: 1px;
        background-color:rgba(255,255,255,255)''')


app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
application = MainWindow()
application.show()

app.exec()
