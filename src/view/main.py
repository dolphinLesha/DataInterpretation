import datetime
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QObject, pyqtSignal, Qt
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
from src.view.tasks.task3_gui import WidgetStatistics
from tasks.task1_gui import (
    WidgetPlotDraw1,
)
from tasks.task2_gui import (
    WidgetPlotDrawRandom,
)


class Communicate(QObject):

    changeTab = pyqtSignal()


class Route:
    # widgets: list[QWidget]
    index: int
    communicator: Communicate

    def __init__(self):
        self.widgets = []
        self.communicator = Communicate()
        self.widgets.append(WidgetPlotDraw1())
        self.widgets.append(WidgetPlotDrawRandom())
        self.widgets.append(WidgetStatistics())
        self.index = 0


class RoutingWidget(QWidget, Route):
    def __init__(self):
        super().__init__()
        box = SelfVLayout()
        self.setLayout(box)
        tabs = QWidget()
        tabs.setFixedWidth(400)
        self.tabs_box = SelfHLayout(spacing=7)
        tabs.setLayout(self.tabs_box)
        box.addWidget(tabs)
        self.tabs_b = {}
        for i in range(self.widgets.__len__()):
            nam = 'but_' + str(i)
            self.tabs_b[nam] = QPushButton(str(i+1) + " Задание")
            self.tabs_b[nam].setObjectName(str(i))
            self.tabs_b[nam].clicked.connect(self.tab_clicked)
            self.tabs_b[nam].setFixedHeight(30)
            self.tabs_box.addWidget(self.tabs_b[nam])

            self.tabs_b[nam].setStyleSheet('''QPushButton{background-color: rgb(205,235,235);
            border-style: outset;
            border-width: 0px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-color: rgb(150,150,150);
            font: 14px "Microsoft JhengHei UI";
            color: rgb(60,60,60);}
            QPushButton:hover{background-color: rgb(195,225,225);}
            QPushButton:pressed{background-color: rgb(195,215,215);
            }''')
            self.tabs_b[nam].setFixedWidth(80)
        self.tabs_box.setAlignment(Qt.AlignLeft)
        nam = 'but_' + str(0)
        self.tabs_b[nam].setStyleSheet('''QPushButton{background-color: rgb(105,155,155);
            border-style: outset;
            border-width: 0px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-color: rgb(150,150,150);
            font: 14px "Microsoft JhengHei UI";
            color: rgb(60,60,60);}
            QPushButton:hover{background-color: rgb(95,145,145);}
            QPushButton:pressed{background-color: rgb(95,125,125);
                    }''')
        self.tabs_b[nam].setFixedWidth(100)
        self.init_style_sheet()

    def init_style_sheet(self):
        print("tuttt")
        self.setStyleSheet('''QWidget{background-color: rgb(0,0,0);}''')

    def tab_clicked(self):
        sender = self.sender()
        nam = 'but_' + str(self.index)
        self.tabs_b[nam].setStyleSheet('''QPushButton{background-color: rgb(205,235,235);
            border-style: outset;
            border-width: 0px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-color: rgb(150,150,150);
            font: 14px "Microsoft JhengHei UI";
            color: rgb(60,60,60);}
            QPushButton:hover{background-color: rgb(195,225,225);}
            QPushButton:pressed{background-color: rgb(195,215,215);
            }''')
        self.tabs_b[nam].setFixedWidth(80)
        self.index = int(sender.objectName())
        nam = 'but_' + str(self.index )
        self.tabs_b[nam].setStyleSheet('''QPushButton{background-color: rgb(105,155,155);
            border-style: outset;
            border-width: 0px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-color: rgb(150,150,150);
            font: 14px "Microsoft JhengHei UI";
            color: rgb(60,60,60);}
            QPushButton:hover{background-color: rgb(95,145,145);}
            QPushButton:pressed{background-color: rgb(95,125,125);
            }''')
        self.tabs_b[nam].setFixedWidth(100)
        self.communicator.changeTab.emit()


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(str(datetime.datetime.now()))
        self.setFixedWidth(1280)
        # self.setFixedHeight(900)
        self.route = RoutingWidget()
        self.init_ui()
        self.init_style_sheet()

    def init_ui(self):
        self.route.communicator.changeTab.connect(self.changeTab)
        self.main_v_box = SelfVLayout(margin=Vector4().symmetric(10, 0))
        self.setLayout(self.main_v_box)
        self.route.setFixedHeight(35)
        self.main_widget = self.route.widgets[self.route.index]
        self.main_widget_copy = self.main_widget
        self.main_v_box.addWidget(self.route)
        self.main_v_box.addWidget(self.main_widget)

    def init_style_sheet(self):
        self.route.setStyleSheet('''border-bottom: 1px solid rgba(0,0,0,50);''')
        self.setStyleSheet('''QWidget#plot{background-color: rgba(0,255,255,255);}''')

    def changeTab(self):
        print('tut')
        # self.main_v_box.addWidget(self.route)
        self.main_v_box.removeWidget(self.main_widget)
        self.main_widget.setParent(None)
        self.main_widget.destroy()
        self.main_widget = self.route.widgets[self.route.index]
        self.main_v_box.addWidget(self.main_widget)


# class MainWindow2(QWidget):
#     def __init__(self):
#         super(MainWindow2, self).__init__()
#         self.lay = SelfVLayout()
#         self.setLayout(self.lay)
#         self.wid1 = QTextEdit("as")
#         self.wid2 = QPushButton("Press")
#         self.lay.addWidget(self.wid1)
#         self.lay.addWidget(self.wid2)
#         self.wid2.clicked.connect(self.switch)
#
#     def switch(self):
#         self.lay.removeWidget(self.wid2)
#         self.wid2.setParent(None)
#         self.wid2.destroy()


app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
application = MainWindow()
application.show()

app.exec()
