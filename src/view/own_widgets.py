from copy import deepcopy
from typing import Any, Union

import pyperclip as pc
import pyqtgraph as pg
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QFrame, QGroupBox, QLineEdit, QPushButton, QComboBox, \
    QLabel, QScrollArea, QFileDialog

from src.control.audio.audio_function import AudioFunction
from src.control.audio.audio_module import AudioModule
from src.control.file_read import FileReader
from src.control.function import Function
from src.data.graphic import Variants
from src.data.klasses import Vector4
from src.data.tasks.default_values import *
from src.view.view_settings import ViewSettings


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


class SelfPlot(QWidget):

    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        vbox = SelfVLayout()
        self.setLayout(vbox)
        self.plot = pg.PlotWidget()
        self.plot.setBackground(QColor(*ViewSettings.background_color))
        # self.plots[kwargs['plot_name']] = pg.PlotWidget()
        # self.plots[kwargs['plot_name']].setBackground('w')
        # self.plots[kwargs['plot_name']].setObjectName(kwargs['plot_name'])
        title = QLabel(title)
        title.setFixedHeight(13)
        title.setStyleSheet('''QLabel{
                font: 12px "Microsoft JhengHei UI";
                color: rgba(%d, %d, %d, 230);
                text-align: center;
                }''' % ViewSettings.foreground_color)
        title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.plot, stretch=10)
        vbox.addWidget(title, stretch=1)


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
        # self.setStyleSheet('''
        # QGroupBox{
        # border: 1px solid rgba(0,0,0,122);
        # }
        # QGroupBox::title{
        # subcontrol-position: top left;
        # padding: 0 -9px;
        # }
        # ''')
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
        self.setStyleSheet('''QGroupBox{
                border: 0px solid;
                margin-top: 5ex;}
                QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left; /* position at the top center */
                padding: -15ex 5px;
                color: rgb(%d,%d,%d);
                }
                    ''' % ViewSettings.foreground_color2)

    def get_value(self):
        if self.lineEdit.text().isnumeric():
            return self.lineEdit.text()
        return None

    def get_value_as_int(self):
        if self.lineEdit.text().replace('-', '').isnumeric():
            return int(self.lineEdit.text())
        return None

    def get_value_as_float(self):
        # if self.lineEdit.text().replace('-', '').replace('.', '').replace(',', '').isnumeric():
        #     return float(self.lineEdit.text().replace(',', '.'))
        try:
            return float(self.lineEdit.text())
        except Exception:

            return None


class SelfLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text: str = ""):
        super(SelfLabel, self).__init__(text)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()


class SelfTitledLabel(QGroupBox):

    def __init__(self, title: str, text: str = "", width: int = None):
        super(SelfTitledLabel, self).__init__()
        self.setTitle(title)
        lay = SelfVLayout()
        self.setLayout(lay)
        self.label = SelfLabel(text)
        self.label.clicked.connect(self.copy_to_clipboard)
        self.setFixedHeight(45)
        if width:
            self.setFixedWidth(width)

        lay.addWidget(self.label)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QGroupBox{
                border: 0px solid;
                margin-top: 5ex;}
                QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; /* position at the top center */
                padding: 3px;
                color: rgb(%d,%d,%d);
                }
                    ''' % ViewSettings.foreground_color2)
        # self.setContentsMargins(4, 8, 4, 0)
        self.label.setStyleSheet('''QLabel{
        height: 30px;
        font: 14px "Microsoft JhengHei UI";
        color: rgb(%d,%d,%d);
        }
        QLabel:hover{color: rgb(40,40,40);
         font: 18px;
         height: 60px;
        }
        ''' % ViewSettings.foreground_color2)

    def set_text(self, text: str):
        self.label.setText(text)

    def copy_to_clipboard(self):
        pc.copy(self.label.text())


class SelfButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QPushButton{background-color: rgb(105,155,255);
        height: 40px;
        border-style: outset;
        border-width: 0px;
        border-radius: 13px;
        border-color: rgb(90,90,90);
        font: 17px "Microsoft JhengHei UI";
        color: rgb(255,255,255);}
        QPushButton:hover{background-color: rgb(90,90,250);
        color: rgb(255,255,255);}
        QPushButton:pressed{background-color: rgb(70,170,200);
        color: rgb(255,255,255);}
        QPushButton:disabled{background-color: rgb(180,180,180);
        color: rgb(255,255,255);}''')


class SelfButton2(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet(ViewSettings.self_button2)


class SelfControlPanel(QWidget):
    """
    Боковая панель настроек вкладки приложения
    """

    def __init__(self):
        super().__init__()
        self.setObjectName('control_panel')
        self.vlay_main = SelfVLayout()
        self.setLayout(self.vlay_main)

        self.scroll_w = QScrollArea()
        # self.scroll_w.setFixedHeight(500)
        self.scroll_w.setWidgetResizable(True)
        self.w = QWidget()
        self.scroll_w.setWidget(self.w)

        self.vlay = SelfVLayout(spacing=10)
        self.w.setLayout(self.vlay)

        self.vlay_main.addWidget(self.scroll_w)
        self.init_style_sheet()

    def add_widget(self, widget: QWidget):
        print(widget.objectName())
        self.vlay.addWidget(widget)

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#control_panel{
            border: 0px;
        }''')
        self.scroll_w.setStyleSheet('''QScrollArea{
            border: 0px;
        }''')


class SelfComboBoxFunctions(QComboBox):
    """
    Вспомогательный класс виджета с выбором функций для построения
    """

    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        for key, val in Variants.func_variants.items():
            self.addItem(key)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QComboBox {
            font: 17px "Microsoft JhengHei UI";

        }
        QComboBox QAbstractItemView {
            selection-background-color: rgba(150,150,150,40);
            selection-border: 0px solid gray;
            selection-color: rgb(0,0,0);
        }
        ''')


class SelfComboBoxLoadVariants(QComboBox):
    """
    Вспомогательный класс для выбора загрузки функции из приложения, файла с готовой функцией или звукового файла
    """

    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.addItem('Встроенные функции', 'build-in function')
        self.addItem('Загрузить из файла', 'load from file')
        self.addItem('Загрузить из wav', 'load from wav')
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QComboBox {
            font: 17px "Microsoft JhengHei UI";

        }
        QComboBox QAbstractItemView {
            selection-background-color: rgba(150,150,150,40);
            selection-border: 0px solid gray;
            selection-color: rgb(0,0,0);
        }
        ''')


class SelfFuncGeneralSettings(QGroupBox):
    """
    Класс для генерации настроек функции

    У каждой функции есть свои параметры, к примеру длина, параметр частоты, амплитуды, максимума и тд
    Этот класс генерирует виджет, который бы позволял настраивать любую функцию с любыми параметрами, используя их настройки

    Он и позволяет подключить построение любой встроенной функции в приложении, чтобы не выбирать их вручную из кода
    """

    def __init__(self, **kwargs):
        super(SelfFuncGeneralSettings, self).__init__()
        title = kwargs.get('widget_title')
        self.setObjectName('settings')
        if title is None:
            title = ''
            # raise Exception('Не задано поле widget_title')

        self.graphic_title = kwargs.get('graphic_title')
        atr = kwargs.get('atr')
        if atr is None:
            raise Exception('Не заданы аттрибуты')
        atr = dict(atr)

        self.setTitle(title)
        lay = SelfVLayout()
        self.setLayout(lay)
        self.k_types = []
        for k, v in atr.items():
            dct = dict(v)
            title = str(dct.get('title'))
            ret_name = str(dct.get('ret_name'))
            if ret_name is None:
                raise Exception(f'ret_name doesnt setted to {k}')
            default_value = dct.get('default_value')
            hint_text = str(default_value)
            type_type = dct.get('type_type')
            if type_type is None:
                raise Exception(f'type_type doesnt setted to {k}')
            ledit = SelfTitledLineEdit(title=title, hint_text=hint_text)
            self.__setattr__(k, ledit)
            lay.addWidget(ledit)
            self.k_types.append(tuple([ret_name, type_type, default_value]))

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QGroupBox#settings{
        border: 0px solid;
        margin-top: 3ex;}
        QGroupBox#settings::title {
        subcontrol-origin: margin;
        subcontrol-position: top center; /* position at the top center */
        padding: 0 3px;
        color: rgb(%d,%d,%d);
        }
            ''' % ViewSettings.foreground_color2)

    def _set_values(self):
        self._result_dict = {'title': self.graphic_title}
        i = 0
        for k, v in self.__dict__.items():
            if k[0:2] != 'p_':
                continue
            q_object = self.__getattribute__(k)
            if self.k_types[i][1] == int:
                val = q_object.get_value_as_int()
            elif self.k_types[i][1] == float:
                val = q_object.get_value_as_float()
            else:
                raise NotImplemented('no types')
            if val is None:
                val = self.k_types[i][2]
            self._result_dict[self.k_types[i][0]] = val
            i += 1

    def get_values(self) -> dict[str, Any]:
        self._set_values()
        print(self._result_dict)
        return self._result_dict


class FuncSettings:
    """
    Класс, в котором перечислены все необходимые настройки, параметры функции для виджета настройки функции
    """
    def __init__(self):
        self.lin_settings = {
            'widget_title': 'Настройки',
            'graphic_title': 'Линейная функция',
            'atr': {
                'p_parameter_n_input': {
                    'title': 'n',
                    'ret_name': 'n',
                    'default_value': DefaultTask1.n,
                    'type_type': int
                },
                'p_parameter_a_input': {
                    'title': 'a',
                    'ret_name': 'a',
                    'default_value': DefaultTask1.a,
                    'type_type': float
                },
                'p_parameter_b_input': {
                    'title': 'b',
                    'ret_name': 'b',
                    'default_value': DefaultTask1.b,
                    'type_type': float
                }
            }
        }

        self.exp_settings = {
            'widget_title': 'Настройки',
            'graphic_title': 'Экспонента',
            'atr': {
                'p_parameter_n_input': {
                    'title': 'n',
                    'ret_name': 'n',
                    'default_value': DefaultTask1.n,
                    'type_type': int
                },
                'p_parameter_a_input': {
                    'title': 'a',
                    'ret_name': 'a',
                    'default_value': DefaultTask1.a,
                    'type_type': float
                },
                'p_parameter_b_input': {
                    'title': 'b',
                    'ret_name': 'b',
                    'default_value': DefaultTask1.b,
                    'type_type': float
                }
            }
        }

        self.rand_settings = {
            'widget_title': 'Настройки',
            'graphic_title': 'Рандом',
            'atr': {
                'p_parameter_n_input': {
                    'title': 'n',
                    'ret_name': 'n',
                    'default_value': DefaultTask2.n,
                    'type_type': int
                },
                'p_parameter_min_input': {
                    'title': 'min',
                    'ret_name': 'min_p',
                    'default_value': DefaultTask2.min_p,
                    'type_type': float
                },
                'p_parameter_max_input': {
                    'title': 'max',
                    'ret_name': 'max_p',
                    'default_value': DefaultTask2.max_p,
                    'type_type': float
                }
            }
        }

        self.rand_add_settings = deepcopy(self.rand_settings)
        self.rand_add_settings['title'] = 'Рандом с накоплениями'
        self.rand_add_settings['atr'].update(
            {
                'p_parameter_amount_input': {
                    'title': 'Накоплений',
                    'ret_name': 'amount',
                    'default_value': 0,
                    'type_type': int
                }
            }
        )
        self.rand_own_setting = deepcopy(self.rand_settings)
        self.rand_own_setting['title'] = 'Рандом свой'
        self.rand_own_setting['graphic_title'] = 'Рандом свой'
        self.rand_own_setting['atr'].update(
            {
                'p_parameter_precision_input': {
                    'title': 'Precision',
                    'ret_name': 'precision',
                    'default_value': DefaultTask2.precision,
                    'type_type': int
                }
            }
        )

        self.harm_settings = {
            'widget_title': 'Настройки',
            'graphic_title': 'Гармоника',
            'atr': {
                'p_parameter_n_input': {
                    'title': 'n',
                    'ret_name': 'n',
                    'default_value': DefaultTask5.n,
                    'type_type': int
                },
                'p_parameter_a_input': {
                    'title': 'a',
                    'ret_name': 'a1',
                    'default_value': DefaultTask5.a1,
                    'type_type': float
                },
                'p_parameter_f_input': {
                    'title': 'f',
                    'ret_name': 'f1',
                    'default_value': DefaultTask5.f1,
                    'type_type': float
                },
                'p_parameter_dt_input': {
                    'title': 'dt',
                    'ret_name': 'dt',
                    'default_value': DefaultTask5.dt,
                    'type_type': float
                }
            }
        }

        self.rythm_settings = {
            'widget_title': 'Настройки',
            'graphic_title': 'Ритм',
            'atr': {
                'p_parameter_n_input': {
                    'title': 'n',
                    'ret_name': 'n',
                    'default_value': DefaultRythmFunction.n,
                    'type_type': int
                },
                'p_parameter_a_input': {
                    'title': 'a',
                    'ret_name': 'a1',
                    'default_value': DefaultRythmFunction.a1,
                    'type_type': float
                },
                'p_parameter_f_input': {
                    'title': 'f',
                    'ret_name': 'f1',
                    'default_value': DefaultRythmFunction.f1,
                    'type_type': float
                },
                'p_parameter_dt_input': {
                    'title': 'dt',
                    'ret_name': 'dt',
                    'default_value': DefaultRythmFunction.dt,
                    'type_type': float
                }
            }
        }

        self.harm_rand_settings = deepcopy(self.harm_settings)
        self.harm_rand_settings['title'] = 'Гармоника с шумами'
        self.harm_rand_settings['graphic_title'] = 'Гармоника с шумами'
        self.harm_rand_settings['atr'].update(
            {
                'p_parameter_max_input': {
                    'title': 'max',
                    'ret_name': 'max_p',
                    'default_value': DefaultTask2.max_p,
                    'type_type': float
                }
            }
        )
        self.harm_rand_settings['atr'].update(
            {
                'p_parameter_min_input': {
                    'title': 'min',
                    'ret_name': 'min_p',
                    'default_value': DefaultTask2.min_p,
                    'type_type': float
                }
            }
        )

        self.harm_rand_add_settings = deepcopy(self.harm_rand_settings)
        self.harm_rand_add_settings['title'] = 'Гармоника шум, добавление'
        self.harm_rand_add_settings['atr'].update(
            {
                'p_parameter_amount_input': {
                    'title': 'Накоплений',
                    'ret_name': 'amount',
                    'default_value': 0,
                    'type_type': int
                }
            }
        )

        self.poly_harm_settings = deepcopy(self.harm_settings)
        # self.poly_harm_settings['title'] = 'Полигармоника'
        self.poly_harm_settings['graphic_title'] = 'Полигармоника'
        self.poly_harm_settings['atr'].update(
            {
                'p_parameter_a2_input': {
                    'title': 'a2',
                    'ret_name': 'a2',
                    'default_value': DefaultTask5.a2,
                    'type_type': float
                }
            }
        )
        self.poly_harm_settings['atr'].update(
            {
                'p_parameter_f2_input': {
                    'title': 'f2',
                    'ret_name': 'f2',
                    'default_value': DefaultTask5.f2,
                    'type_type': float
                }
            }
        )
        self.poly_harm_settings['atr'].update(
            {
                'p_parameter_a3_input': {
                    'title': 'a3',
                    'ret_name': 'a3',
                    'default_value': DefaultTask5.a3,
                    'type_type': float
                }
            }
        )
        self.poly_harm_settings['atr'].update(
            {
                'p_parameter_f3_input': {
                    'title': 'f3',
                    'ret_name': 'f3',
                    'default_value': DefaultTask5.f3,
                    'type_type': float
                }
            }
        )
        self.fnch_settings = {
            'widget_title': 'Настройки',
            'graphic_title': 'ФНЧ',
            'atr': {
                'p_parameter_m_input': {
                    'title': 'm',
                    'ret_name': 'm',
                    'default_value': DefaultImpulseReactionFunction.m,
                    'type_type': int
                },
                'p_parameter_fc_input': {
                    'title': 'fc',
                    'ret_name': 'fc',
                    'default_value': DefaultImpulseReactionFunction.fc,
                    'type_type': float
                },
                'p_parameter_dt_input': {
                    'title': 'dt',
                    'ret_name': 'dt',
                    'default_value': DefaultImpulseReactionFunction.dt,
                    'type_type': float
                }
            }
        }

        self.lpf_sym_settings = deepcopy(self.fnch_settings)
        self.lpf_sym_settings['graphic_title'] = 'ФНЧ (сим)'

        self.hpf_sym_settings = deepcopy(self.fnch_settings)
        self.hpf_sym_settings['graphic_title'] = 'ФВЧ (сим)'

        self.bpf_sym_settings = deepcopy(self.fnch_settings)
        self.bpf_sym_settings['graphic_title'] = 'ПФ (сим)'
        self.bpf_sym_settings['atr'].update(
            {
                'p_parameter_fc_input': {
                    'title': 'fc1',
                    'ret_name': 'fc1',
                    'default_value': DefaultImpulseReactionFunction.fc1,
                    'type_type': float
                },
                'p_parameter_fc2_input': {
                    'title': 'fc2',
                    'ret_name': 'fc2',
                    'default_value': DefaultImpulseReactionFunction.fc2,
                    'type_type': float
                },
            }
        )

        self.bsf_sym_settings = deepcopy(self.bpf_sym_settings)
        self.bsf_sym_settings['graphic_title'] = 'РФ (сим)'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(FuncSettings, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class SelfRandomAddFuncSettings(SelfFuncGeneralSettings):

    def __init__(self, **kwargs):
        super(SelfRandomAddFuncSettings, self).__init__(**kwargs)

    def _set_values(self):
        super(SelfRandomAddFuncSettings, self)._set_values()
        min_p = self._result_dict['min_p']
        max_p = self._result_dict['max_p']
        self._result_dict['graph_limit'] = (min_p, max_p)
        self._result_dict['title'] = 'n= ' + \
                                     str(self._result_dict['amount'])


class SelfRandomOwnFuncSettings(SelfFuncGeneralSettings):

    def __init__(self, **kwargs):
        super(SelfRandomOwnFuncSettings, self).__init__(**kwargs)

    def _set_values(self):
        super(SelfRandomOwnFuncSettings, self)._set_values()
        self._result_dict['precision'] = 10 ** self._result_dict['precision']


class SelfHarmonicRandAddFuncSettings(SelfFuncGeneralSettings):

    def __init__(self, **kwargs):
        super(SelfHarmonicRandAddFuncSettings, self).__init__(**kwargs)

    def _set_values(self):
        super(SelfHarmonicRandAddFuncSettings, self)._set_values()
        a1 = self._result_dict['a1']
        min_p = self._result_dict['min_p']
        max_p = self._result_dict['max_p']
        self._result_dict['graph_limit'] = (-a1 + min_p, a1 + max_p)
        self._result_dict['title'] = 'n= ' + \
                                     str(self._result_dict['amount'])


class SelfFuncSettings:
    """
    Все настройки, чтобы к ним можно обращаться как к массиву
    """
    def __init__(self):
        self.settings = []
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().lin_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().exp_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().rand_settings))
        self.settings.append(SelfRandomAddFuncSettings(**FuncSettings().rand_add_settings))
        self.settings.append(SelfRandomOwnFuncSettings(**FuncSettings().rand_own_setting))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().harm_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().harm_rand_settings))
        self.settings.append(SelfHarmonicRandAddFuncSettings(**FuncSettings().harm_rand_add_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().poly_harm_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().rythm_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().fnch_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().lpf_sym_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().hpf_sym_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().bpf_sym_settings))
        self.settings.append(SelfFuncGeneralSettings(**FuncSettings().bsf_sym_settings))


class SelfFuncSettingsWidget(QWidget):
    """Виджет, который позволяет выбирать функцию, и возвращает ее или ее настройки"""
    def __init__(self):
        super(SelfFuncSettingsWidget, self).__init__()
        self.lay = SelfVLayout()
        self.setLayout(self.lay)

        self.combo_box = SelfComboBoxFunctions()
        self.combo_box.setFixedWidth(200)
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
        return list(Variants.func_variants.values())[self.combo_box.currentIndex()]


class SelfFunctionCreateVariant(QWidget):
    """
    Виджет, который позволяет выбрать, откуда брать функцию: из готовых, из файла или из звукового файла
    Возвращает построенную функцию, ее настройки, если бралась из приложения

    Если загружается звуковой файл, то возвращается единственный или усредненный канал
    """
    def __init__(self):
        super(SelfFunctionCreateVariant, self).__init__()
        self.lay = SelfVLayout()
        self.setLayout(self.lay)

        self.combo_box = SelfComboBoxLoadVariants()
        self.combo_box.setFixedWidth(200)
        self.combo_box.currentIndexChanged.connect(self.variant_changed)
        self.lay.addWidget(self.combo_box)
        self.variant_settings = SelfFuncSettingsWidget()
        self.lay.addWidget(self.variant_settings)

    def variant_changed(self, index: int):
        self.variant_settings.setParent(None)
        if index == 0:
            self.variant_settings = SelfFuncSettingsWidget()
        elif index == 1:
            self.variant_settings = SelfFileOpenPicker('Загрузить данные')
        elif index == 2:
            self.variant_settings = SelfFileLoad()
        self.lay.addWidget(self.variant_settings)
        # self.lay.setStretch(0, 1)

    def get_settings(self) -> dict[str, Any]:
        if isinstance(self.variant_settings, SelfFuncSettingsWidget):
            return self.variant_settings.get_settings()

    def get_function(self) -> Function:
        if isinstance(self.variant_settings, SelfFuncSettingsWidget):
            func = self.variant_settings.get_function()
            func.build(**self.get_settings())
            return func
        elif isinstance(self.variant_settings, SelfFileOpenPicker):
            func = self.variant_settings.get_function_data()
            return func
        elif isinstance(self.variant_settings, SelfFileLoad):
            path = self.variant_settings.path

            wav_file = AudioModule().read(path)
            self.audio_func = AudioFunction()
            self.audio_func.build_from_wav_file(wav_file=wav_file)

            if self.audio_func.channels == 2:
                self.func_l = self.audio_func.common_channel
                self.func_r = self.audio_func.right_channel
                self.func_a = self.func_l.average(self.func_r)
                return self.func_a
            else:
                self.func_a = self.audio_func.common_channel
                return self.func_a
        else:
            raise Exception('none')
        # return list(Variants().func_variants.values())[self.combo_box.currentIndex()]


class SelfSpikesFuncSettings(QGroupBox):

    def __init__(self):
        super(SelfSpikesFuncSettings, self).__init__()
        self.setTitle("Настройки")
        lay = SelfVLayout()
        self.setLayout(lay)
        self.parameter_n_input = SelfTitledLineEdit(title=" n", hint_text="5")
        self.parameter_val_input = SelfTitledLineEdit(title=" val", hint_text="1000")
        self.parameter_d_input = SelfTitledLineEdit(title=" d", hint_text="100")

        lay.addWidget(self.parameter_n_input)
        lay.addWidget(self.parameter_val_input)
        lay.addWidget(self.parameter_d_input)

        self.init_style_sheet()

    def init_style_sheet(self):
        pass

    def get_values(self) -> dict[str, Any]:
        n = self.parameter_n_input.get_value_as_int()
        if n is None:
            n = DefaultTask6.n
        val = self.parameter_val_input.get_value_as_int()
        if val is None:
            val = DefaultTask6.val
        d = self.parameter_d_input.get_value_as_int()
        if d is None:
            d = DefaultTask6.d
        return {'n': n, 'val': val, 'd': d}


class SelfGroupBox(QGroupBox):
    def __init__(self, title: str):
        super(SelfGroupBox, self).__init__()
        self.setTitle(title)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QGroupBox{
                border: 0px solid;
                margin-top: 5ex;
                background-color: rgb(%d,%d,%d);}
                QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; /* position at the top center */
                padding: 3px;
                color: rgb(%d,%d,%d);
                }
        ''' % (ViewSettings.background_color[0], ViewSettings.background_color[1],
               ViewSettings.background_color[2], ViewSettings.foreground_color2[0],
               ViewSettings.foreground_color2[1], ViewSettings.foreground_color2[2]))


class SelfFileOpenPicker(QPushButton):
    """
    Кнопка загрузки функции из файла
    """
    def __init__(self, name: str = '', callback=None):
        super(SelfFileOpenPicker, self).__init__(name)
        if callback is not None:
            self.callback = callback
        self.clicked.connect(self.open_file_name_dialog)

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Binary files (*.dat *.bin)", options=options)
        if file_name:
            self.path = file_name
            print('callback')
            print(file_name)
            self.callback(file_name)

    def get_path(self):
        if hasattr(self, 'path'):
            return self.path
        return None

    def get_function_data(self) -> Function:
        reader = FileReader(self.path)
        func = reader.load_data()

        return func


class SelfFileSavePicker(QPushButton):
    """
    Кнопка для сохранения чего либо (возвращает путь с именем файла, который выбрал пользователь)
    """
    def __init__(self, name: str = '', callback=None):
        super(SelfFileSavePicker, self).__init__(name)
        if callback is not None:
            self.callback = callback
        self.clicked.connect(self.save_file_name_dialog)

        self.init_style_sheet()

    def save_file_name_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;Wav files (*.wav)", options=options)
        if file_name:
            self.path = file_name
            # self.callback()
            print(file_name)

    def get_path(self):
        if hasattr(self, 'path'):
            return self.path
        return None

    def init_style_sheet(self):
        self.setStyleSheet(ViewSettings.self_button2)


class SelfFileLoad(QGroupBox):
    """
    Для получения пути файла, который пользователь выбрал для загрузки
    """

    def __init__(self):
        super(SelfFileLoad, self).__init__()
        self.setTitle("Загрузка файла")
        lay = SelfVLayout()
        self.setLayout(lay)

        def set_file(path: str):
            print('set_file')
            print(path)
            self.path = path
            print(self.path)
            label_name = self.path.split('/')[-1]
            self.file_label.set_text(label_name)

        self.file_picker = SelfFileOpenPicker('загрузить', set_file)
        self.file_label = SelfTitledLabel('имя', '')

        lay.addWidget(self.file_picker)
        lay.addWidget(self.file_label)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QGroupBox{
                border: 0px solid;
                margin-top: 5ex;}
                QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; /* position at the top center */
                padding: 3px;
                color: rgb(%d,%d,%d);
                }
                    ''' % ViewSettings.foreground_color2)


class SelfComboBoxProcessing(QComboBox):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        for key, val in Variants.proc_variants.items():
            self.addItem(val)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QComboBox {
            font: 17px "Microsoft JhengHei UI";

        }
        QComboBox QAbstractItemView {
            selection-background-color: rgba(150,150,150,40);
            selection-border: 0px solid gray;
            selection-color: rgb(0,0,0);
        }
        ''')


class SelfFuncProcessingWidget(QWidget):
    """
    Виджет, который позволяет выбирать операции для преобразования
    """
    def __init__(self):
        super(SelfFuncProcessingWidget, self).__init__()
        self.lay = SelfVLayout()
        self.setLayout(self.lay)

        self.combo_box = SelfComboBoxProcessing()
        # self.combo_box.setFixedWidth(200)
        self.combo_box.currentIndexChanged.connect(self.proc_changed)
        self.combo_box.setCurrentIndex(1)
        self.lay.addWidget(self.combo_box)
        self.index = 1
        self.variant_settings = SelfFunctionCreateVariant()
        self.lay.addWidget(self.variant_settings)

    def proc_changed(self, index: int):
        self.index = index
        self.variant_settings.setParent(None)
        if list(Variants.proc_variants.keys())[index] in ('add_func', 'multi', 'convolve'):
            self.variant_settings = SelfFunctionCreateVariant()
        elif list(Variants.proc_variants.keys())[index] == 'rmv_white_noise':
            self.variant_settings = SelfTitledLineEdit('p', '0')
        self.lay.addWidget(self.variant_settings)

    def get_settings(self) -> Union[dict[str, Any], float, int]:
        if isinstance(self.variant_settings, SelfTitledLineEdit):
            return self.variant_settings.get_value_as_float()
        return self.variant_settings.get_values()

    def get_function(self) -> Function:
        if isinstance(self.variant_settings, SelfFunctionCreateVariant):
            return self.variant_settings.get_function()

    def get_proc(self):
        return list(Variants.proc_variants.keys())[self.combo_box.currentIndex()]
