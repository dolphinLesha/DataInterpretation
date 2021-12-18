import datetime
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject, pyqtSignal

from src.view.own_widgets import *
from src.view.tasks.project_gui import WidgetProject
from src.view.tasks.task10_gui import WidgetTask10
from src.view.tasks.task3_gui import WidgetStatistics
from src.view.tasks.task4_gui import WidgetTask4
from src.view.tasks.task5_gui import WidgetTask5
from src.view.tasks.task6_gui import WidgetTask6
from src.view.tasks.task7_gui import WidgetTask7
from src.view.tasks.task8_gui import WidgetTask8
from src.view.tasks.task9_gui import WidgetTask9
from src.view.view_settings import ViewSettings
from tasks.task1_gui import (
    WidgetPlotDraw1,
)
from tasks.task2_gui import (
    WidgetPlotDrawRandom,
)


class Communicate(QObject):
    changeTab = pyqtSignal()


class Route:
    """
    Класс для маршрутизации окон в приложении
    """
    index: int
    communicator: Communicate

    def __init__(self):
        """
        Инициализируем коммуникатор и все вкладки приложения
        """
        self.widgets = []
        self.communicator = Communicate()
        self.widgets.append(WidgetPlotDraw1())
        self.widgets.append(WidgetPlotDrawRandom())
        self.widgets.append(WidgetStatistics())
        self.widgets.append(WidgetTask4())
        self.widgets.append(WidgetTask5())
        self.widgets.append(WidgetTask6())
        self.widgets.append(WidgetTask7())
        self.widgets.append(WidgetTask8())
        self.widgets.append(WidgetTask9())
        self.widgets.append(WidgetTask10())
        self.widgets.append(WidgetProject())
        self.index = 0


class RoutingWidget(QWidget, Route):
    """
    Класс управления маршрутизацией

    Здесь генерируются кнопки верхней панели приложения, которые отвечают за вкладки
    """
    def __init__(self):
        super().__init__()
        box = SelfVLayout()
        self.setLayout(box)
        tabs = QWidget()
        tabs.setFixedWidth(1200)
        self.tabs_box = SelfHLayout(spacing=2)
        tabs.setLayout(self.tabs_box)
        box.addWidget(tabs)
        self.tabs_b = {}
        for i in range(self.widgets.__len__()):
            nam = 'but_' + str(i)
            self.tabs_b[nam] = QPushButton(str(i + 1) + " Задание")
            if i == 10:
                self.tabs_b[nam] = QPushButton('проект')
            self.tabs_b[nam].setObjectName(str(i))
            self.tabs_b[nam].clicked.connect(self.tab_clicked)
            self.tabs_b[nam].setFixedHeight(30)
            self.tabs_box.addWidget(self.tabs_b[nam])

            self.tabs_b[nam].setStyleSheet(ViewSettings.tab_button_design_taped)
            self.tabs_b[nam].setFixedWidth(80)
        self.tabs_box.setAlignment(Qt.AlignLeft)
        nam = 'but_' + str(0)
        self.tabs_b[nam].setStyleSheet(ViewSettings.tab_button_design_no_taped)
        self.tabs_b[nam].setFixedWidth(100)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget{background-color: rgb(0,0,0);}''')

    def tab_clicked(self):
        sender = self.sender()
        nam = 'but_' + str(self.index)
        self.tabs_b[nam].setStyleSheet(ViewSettings.tab_button_design_taped)
        self.tabs_b[nam].setFixedWidth(80)
        self.index = int(sender.objectName())
        nam = 'but_' + str(self.index)
        self.tabs_b[nam].setStyleSheet(ViewSettings.tab_button_design_no_taped)
        self.tabs_b[nam].setFixedWidth(100)
        self.communicator.changeTab.emit()


class MainWindow(QWidget):
    """
    Главное окно, корень дерева виджетов
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle(str(datetime.datetime.now()))
        self.setObjectName('mainn')
        # self.setFixedWidth(1280)
        # self.setFixedHeight(900)
        self.route = RoutingWidget()
        self.init_ui()
        self.init_style_sheet()

    def init_ui(self):
        self.route.communicator.changeTab.connect(self.change_tab)
        self.main_v_box = SelfVLayout(margin=Vector4().symmetric(10, 0))
        self.setLayout(self.main_v_box)
        self.route.setFixedHeight(45)
        self.main_widget = self.route.widgets[self.route.index]
        self.main_widget_copy = self.main_widget
        self.main_v_box.addWidget(self.route)
        self.main_v_box.addWidget(self.main_widget)

    def init_style_sheet(self):
        self.route.setStyleSheet('''border-bottom: 1px solid rgba(0,0,0,50);''')
        self.setStyleSheet('''QWidget#plot{background-color: rgba(0,255,255,255);}
        QWidget#mainn{background-color: rgb(%d,%d,%d);}''' % (
        ViewSettings.background_color[0], ViewSettings.background_color[1], ViewSettings.background_color[2]))

    def change_tab(self):
        # self.main_v_box.addWidget(self.route)
        self.main_v_box.removeWidget(self.main_widget)
        self.main_widget.setParent(None)
        self.main_widget.destroy()
        self.main_widget = self.route.widgets[self.route.index]
        self.main_v_box.addWidget(self.main_widget)


app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
application = MainWindow()
application.show()

app.exec()
