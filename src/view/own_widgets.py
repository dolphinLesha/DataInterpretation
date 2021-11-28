from copy import deepcopy
from typing import Any

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QFrame, QGroupBox, QLineEdit, QPushButton, QComboBox, \
    QLabel, QScrollArea, QFileDialog

from src.control.file_read import FileReader
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


class SelfControlPanel(QWidget):
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
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        for key, val in FunctionVariants().variants.items():
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
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.addItem('Встроенные функции', 'build-in function')
        self.addItem('Загрузить из файла', 'load from file')
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
    def __init__(self, **kwargs):
        super(SelfFuncGeneralSettings, self).__init__()
        title = kwargs.get('widget_title')

        if title is None:
            raise Exception('Не задано поле widget_title')

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
        pass

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
        return list(FunctionVariants().variants.values())[self.combo_box.currentIndex()]


class SelfFunctionCreateVariant(QWidget):
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
        else:
            raise Exception('none')
        # return list(FunctionVariants().variants.values())[self.combo_box.currentIndex()]


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


class SelfFileOpenPicker(QPushButton):
    def __init__(self, name: str = ''):
        super(SelfFileOpenPicker, self).__init__(name)
        self.clicked.connect(self.open_file_name_dialog)

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Binary files (*.dat *.bin)", options=options)
        if file_name:
            self.path = file_name
            print(file_name)

    def get_path(self):
        if hasattr(self, 'path'):
            return self.path
        return None

    def get_function_data(self) -> Function:
        reader = FileReader(self.path)
        func = reader.load_data()

        return func
