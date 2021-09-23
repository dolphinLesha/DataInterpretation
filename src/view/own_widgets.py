from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QFrame, QGroupBox, QLineEdit, QPushButton

from src.data.klasses import Vector4


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
        height: 35px;
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
        if self.lineEdit.text().replace('-','').isnumeric():
            return int(self.lineEdit.text())
        return None


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
        color: rgb(255,255,255);}''')
