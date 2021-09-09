from PyQt5 import QtWidgets, QtCore
import sys
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


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Проверка работ")


app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
application = MainWindow()
application.show()

app.exec()
