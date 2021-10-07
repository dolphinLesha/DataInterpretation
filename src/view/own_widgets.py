from typing import Any

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QFrame, QGroupBox, QLineEdit, QPushButton, QComboBox, \
    QLabel

from src.control.function import Function
from src.data.graphic import FunctionVariants
from src.data.klasses import Vector4
from src.data.tasks.default_values import *


class SelfVLayout(QVBoxLayout):

    def __init__(self, parent: QWidget = None, spacing: int = 0, margin: Vector4 = None):
        super().__init__(parent)
        if margin is None:
            margin = Vector4()
        self.setContentsMargins(margin.v1, margin.v2, margin.v3, margin.v4)
        self.setSpacing(spacing)


class SelfHLayout(QHBoxLayout):

    def __init__(self, parent: QWidget = None, spacing: int = 0, margin: Vector4 = None):
        super().__init__(parent)
        if margin is None:
            margin = Vector4()
        self.setContentsMargins(margin.v1, margin.v2, margin.v3, margin.v4)
        self.setSpacing(spacing)


class SelfFrame(QFrame):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)


class SelfTitledLineEdit(QGroupBox):

    def __init__(self, title: str, hint_text: str = None):
        super(SelfTitledLineEdit, self).__init__()
        self.setTitle(title)
        lay = SelfVLayout()
        self.setLayout(lay)
        self.lineEdit = QLineEdit()
        if hint_text is None:
            hint_text = "Введите значение"
        self.lineEdit.setPlaceholderText(hint_text)

        lay.addWidget(self.lineEdit)

        self.init_style_sheet()

    def init_style_sheet(self):
        # self.setContentsMargins(4, 8, 4, 0)
        self.lineEdit.setStyleSheet('''QLineEdit{margin: 4px;
        height: 30px;
        font: 14px "Microsoft JhengHei UI";
        background-color: rgb(240,240,240);
        border: 1px solid rgb(220,220,240);
        border-radius: 7;}
        QLineEdit:hover{background-color: rgb(220,220,220);
        }
        QLineEdit:focus{background-color: rgb(255,255,255);
        }''')

    def get_value(self):
        if self.lineEdit.text().isnumeric():
            return self.lineEdit.text()
        return None

    def get_value_as_int(self):
        if self.lineEdit.text().replace('-', '').isnumeric():
            return int(self.lineEdit.text())
        return None

    def get_value_as_float(self):
        if self.lineEdit.text().replace('-', '').replace('.', '').replace(',', '').isnumeric():
            return float(self.lineEdit.text().replace(',', '.'))
        return None


class SelfTitledLabel(QGroupBox):

    def __init__(self, title: str, text: str = "", width: int = None):
        super(SelfTitledLabel, self).__init__()
        self.setTitle(title)
        lay = SelfVLayout()
        self.setLayout(lay)
        self.label = QLabel(text)
        self.setFixedHeight(45)
        if width:
            self.setFixedWidth(width)

        lay.addWidget(self.label)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QGroupBox{
        border: 1px solid rgb(220,220,240);
        border-radius: 7;
        }
        QGroupBox::title{
        subcontrol-position: top center;
        padding: 0 -9px;
        }''')
        # self.setContentsMargins(4, 8, 4, 0)
        self.label.setStyleSheet('''QLabel{
        height: 30px;
        font: 14px "Microsoft JhengHei UI";
        color: rgb(0,0,0);
        }
        QLabel:hover{color: rgb(40,40,40);
         font: 18px;
         height: 60px;
        }
        ''')

    def set_text(self, text: str):
        self.label.setText(text)


class SelfButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QPushButton{background-color: rgb(105,105,255);
        height: 40px;
        border-style: outset;
        border-width: 0px;
        border-radius: 13px;
        border-color: rgb(90,90,90);
        font: 17px "Microsoft JhengHei UI";
        color: rgb(255,255,255);}
        QPushButton:hover{background-color: rgb(90,90,250);
        color: rgb(255,255,255);}
        QPushButton:pressed{background-color: rgb(70,70,200);
        color: rgb(255,255,255);}
        QPushButton:disabled{background-color: rgb(180,180,180);
        color: rgb(255,255,255);}''')


class SelfComboBoxFunctions(QComboBox):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        for key, val in FunctionVariants().variants.items():
            self.addItem(key)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QComboBox {
            border: 1px solid gray;
            border-bottom-left-radius: 10px;
            border-top-left-radius: 10px;
            padding: 1px 18px 1px 3px;
            font: 17px "Microsoft JhengHei UI";

        }
        QComboBox QAbstractItemView {
            selection-background-color: rgb(50,50,50);
        }
        ''')


class SelfTrendLinFuncSettings(QGroupBox):

    def __init__(self):
        super(SelfTrendLinFuncSettings, self).__init__()
        self.setTitle("Настройки")
        lay = SelfVLayout()
        self.setLayout(lay)
        self.parameter_n_input = SelfTitledLineEdit(title=" N", hint_text="500")
        self.parameter_a_input = SelfTitledLineEdit(title=" a", hint_text="1")
        self.parameter_b_input = SelfTitledLineEdit(title=" b", hint_text="1")

        lay.addWidget(self.parameter_n_input)
        lay.addWidget(self.parameter_a_input)
        lay.addWidget(self.parameter_b_input)

        self.init_style_sheet()

    def init_style_sheet(self):
        pass

    def get_values(self) -> dict[str, Any]:
        n = self.parameter_n_input.get_value_as_int()
        if n is None:
            n = DefaultTask1.n
        a = self.parameter_a_input.get_value_as_float()
        if a is None:
            a = DefaultTask1.a
        b = self.parameter_b_input.get_value_as_float()
        if b is None:
            b = DefaultTask1.b
        return {'n': n, 'a': a, 'b': b}


class SelfTrendExpFuncSettings(QGroupBox):

    def __init__(self):
        super(SelfTrendExpFuncSettings, self).__init__()
        self.setTitle("Настройки")
        lay = SelfVLayout()
        self.setLayout(lay)
        self.parameter_n_input = SelfTitledLineEdit(title=" N", hint_text="500")
        self.parameter_a_input = SelfTitledLineEdit(title=" a", hint_text="1")
        self.parameter_b_input = SelfTitledLineEdit(title=" b", hint_text="1")

        lay.addWidget(self.parameter_n_input)
        lay.addWidget(self.parameter_a_input)
        lay.addWidget(self.parameter_b_input)

        self.init_style_sheet()

    def init_style_sheet(self):
        pass

    def get_values(self) -> dict[str, Any]:
        n = self.parameter_n_input.get_value_as_int()
        if n is None:
            n = DefaultTask1.n
        a = self.parameter_a_input.get_value_as_float()
        if a is None:
            a = DefaultTask1.a
        b = self.parameter_b_input.get_value_as_float()
        if b is None:
            b = DefaultTask1.b
        return {'n': n, 'a': a, 'b': b}


class SelfRandomFuncSettings(QGroupBox):

    def __init__(self):
        super(SelfRandomFuncSettings, self).__init__()
        self.setTitle("Настройки")
        lay = SelfVLayout()
        self.setLayout(lay)
        self.parameter_n_input = SelfTitledLineEdit(title=" N", hint_text="500")
        self.parameter_min_input = SelfTitledLineEdit(title=" Min", hint_text="-1")
        self.parameter_max_input = SelfTitledLineEdit(title=" Max", hint_text="1")

        lay.addWidget(self.parameter_n_input)
        lay.addWidget(self.parameter_min_input)
        lay.addWidget(self.parameter_max_input)

        self.init_style_sheet()

    def init_style_sheet(self):
        pass

    def get_values(self) -> dict[str, Any]:
        n = self.parameter_n_input.get_value_as_int()
        if n is None:
            n = DefaultTask2.n
        min_p = self.parameter_min_input.get_value_as_float()
        if min_p is None:
            min_p = DefaultTask2.min_p
        max_p = self.parameter_max_input.get_value_as_float()
        if max_p is None:
            max_p = DefaultTask2.max_p
        return {'n': n, 'min_p': min_p, 'max_p': max_p}


class SelfRandomOwnFuncSettings(QGroupBox):

    def __init__(self):
        super(SelfRandomOwnFuncSettings, self).__init__()
        self.setTitle("Настройки")
        lay = SelfVLayout()
        self.setLayout(lay)
        self.parameter_n_input = SelfTitledLineEdit(title=" N", hint_text="500")
        self.parameter_min_input = SelfTitledLineEdit(title=" Min", hint_text="-1")
        self.parameter_max_input = SelfTitledLineEdit(title=" Max", hint_text="1")
        self.parameter_precision_input = SelfTitledLineEdit(title=" Precision", hint_text="5")

        lay.addWidget(self.parameter_n_input)
        lay.addWidget(self.parameter_min_input)
        lay.addWidget(self.parameter_max_input)
        lay.addWidget(self.parameter_precision_input)

        self.init_style_sheet()

    def init_style_sheet(self):
        pass

    def get_values(self) -> dict[str, Any]:
        n = self.parameter_n_input.get_value_as_int()
        if n is None:
            n = DefaultTask2.n
        min_p = self.parameter_min_input.get_value_as_float()
        if min_p is None:
            min_p = DefaultTask2.min_p
        max_p = self.parameter_max_input.get_value_as_float()
        if max_p is None:
            max_p = DefaultTask2.max_p
        precision = self.parameter_precision_input.get_value_as_int()
        if precision is None:
            precision = DefaultTask2.precision
        return {'n': n, 'min_p': min_p, 'max_p': max_p, 'precision': 10 ** precision}


class SelfFuncSettings:
    def __init__(self):
        self.settings = []
        self.settings.append(SelfTrendLinFuncSettings())
        self.settings.append(SelfTrendExpFuncSettings())
        self.settings.append(SelfRandomFuncSettings())
        self.settings.append(SelfRandomOwnFuncSettings())


class SelfFuncSettingsWidget(QWidget):
    def __init__(self):
        super(SelfFuncSettingsWidget, self).__init__()
        self.lay = SelfVLayout()
        self.setLayout(self.lay)

        self.combo_box = SelfComboBoxFunctions()
        self.combo_box.currentIndexChanged.connect(self.graph_changed)
        self.lay.addWidget(self.combo_box)
        self.graph_settings = SelfFuncSettings().settings[0]
        self.lay.addWidget(self.graph_settings)

    def graph_changed(self, index: int):
        self.graph_settings.setParent(None)
        self.graph_settings = SelfFuncSettings().settings[index]
        self.lay.addWidget(self.graph_settings)

    def get_settings(self) -> dict[str, Any]:
        return self.graph_settings.get_values()

    def get_function(self) -> Function:
        return list(FunctionVariants().variants.values())[self.combo_box.currentIndex()]