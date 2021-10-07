from PyQt5.QtCore import QSize

from src.control.analysis import AnalysisBuilder
from src.data.graphic import *
from src.view.own_widgets import *


class WidgetTask4(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.init_style_sheet()

    def init_ui(self):
        vbox = SelfVLayout()
        self.setLayout(vbox)
        title = QLabel("Плотность вероятности")
        title.setFixedHeight(30)
        widget = QWidget()
        vbox.addWidget(title)
        vbox.addWidget(widget)
        self.main_h_box = SelfHLayout(spacing=10)
        widget.setLayout(self.main_h_box)
        self.view_graphics = WidgetValues()
        self.view_control = WidgetControl()
        self.view_control.setFixedWidth(200)
        self.view_control.graph_build_b.clicked.connect(self.build_graph)
        self.main_h_box.addWidget(self.view_control)
        self.main_h_box.addWidget(self.view_graphics)

    def init_style_sheet(self):
        # self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
        #         background-color:rgba(255,255,255,255)''')
        self.view_control.setStyleSheet('''QWidget{background-color: rgb(150,150,150);}''')

    def build_graph(self):
        sender = self.sender()

        self.func = self.view_control.graph_and_settings.get_function()
        self.func.build(**self.view_control.graph_and_settings.get_settings())
        Graphic(self.view_graphics.plots["plot1"]).build(func=self.func, prefab=GraphicPrefab.prefab_dark_blue())

        bars = DefaultTask4.bars
        if bars2 := self.view_control.parameter_bar_input.get_value_as_int():
            bars = bars2

        stats = AnalysisBuilder(self.func)
        self.func2 = stats.probability_density(bars)
        Graphic(self.view_graphics.plots["plot3"]).build_histogram(func=self.func2,
                                                                   prefab=GraphicPrefab.prefab_dark_blue())

        self.func3 = stats.auto_correlation_f()
        Graphic(self.view_graphics.plots["plot2"]).build(func=self.func3,
                                                                   prefab=GraphicPrefab.prefab_dark_blue())

        self.func4 = stats.auto_correlation_N_norm_f()
        Graphic(self.view_graphics.plots["plot4"]).build(func=self.func4,
                                                         prefab=GraphicPrefab.prefab_dark_blue())

        self.func5 = self.view_control.graph_and_settings2.get_function()
        self.func5.build(**self.view_control.graph_and_settings2.get_settings())
        Graphic(self.view_graphics.plots["plot5"]).build(func=self.func5, prefab=GraphicPrefab.prefab_dark_blue())

        self.func6 = stats.covariance_f(self.func5)
        Graphic(self.view_graphics.plots["plot6"]).build(func=self.func6,
                                                         prefab=GraphicPrefab.prefab_dark_blue())


class WidgetControl(QWidget):
    def __init__(self, size: QSize = None):
        super().__init__()
        if size is not None:
            self.setFixedSize(size)
        self.setObjectName("z2wid")
        self.init_ui()
        self.init_style_sheet()

    def init_ui(self):
        self.box = SelfVLayout(spacing=15)
        self.setLayout(self.box)
        self.graph_build_b = SelfButton("Построить график")

        '''group box for values of 1 graph'''
        group1 = QGroupBox("Основной график")
        self.box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(self.box_group1)
        self.graph_and_settings = SelfFuncSettingsWidget()
        self.box_group1.addWidget(self.graph_and_settings)

        '''group box for bars'''
        group2 = QGroupBox("Прочие настройки")
        self.box_group2 = SelfVLayout(spacing=5)
        group2.setLayout(self.box_group2)
        self.parameter_bar_input = SelfTitledLineEdit("Кол-во разделений", str(DefaultTask4.bars))
        self.box_group2.addWidget(self.parameter_bar_input)

        '''group box for values of 2 graph'''
        group3 = QGroupBox("Второй график")
        self.box_group3 = SelfVLayout(spacing=5)
        group3.setLayout(self.box_group3)
        self.graph_and_settings2 = SelfFuncSettingsWidget()
        self.box_group3.addWidget(self.graph_and_settings2)

        self.box.addWidget(self.graph_build_b)
        self.box.addWidget(group1)
        self.box.addWidget(group2)
        self.box.addWidget(group3)
        self.box.addStretch(1)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#z2wid{background-color: rgb(150,150,150);}''')
        pass


class WidgetValues(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("plots")
        self.hbox = SelfHLayout(spacing=7)
        self.setLayout(self.hbox)
        self.vbox1 = SelfVLayout()
        self.vbox2 = SelfVLayout()
        self.vbox3 = SelfVLayout()
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox3)
        self.plots = {}
        self.plot1 = self.build_plot_item(plot_name='plot1', plot_title='первый график')
        self.plot1.setFixedSize(450, 320)
        self.plot2 = self.build_plot_item(plot_name='plot2', plot_title='Автокорреляция')
        self.plot2.setFixedSize(450, 220)
        self.plot3 = self.build_plot_item(plot_name='plot3', plot_title='Плотность вероятности')
        self.plot3.setFixedSize(450, 220)
        self.plot4 = self.build_plot_item(plot_name='plot4', plot_title='Автокорреляция по количеству элементов')
        self.plot4.setFixedSize(450, 220)
        self.vbox1.addWidget(self.plot1)
        self.vbox1.addWidget(self.plot3)
        self.vbox1.addWidget(self.plot2)
        self.vbox1.addStretch()

        self.plot5 = self.build_plot_item(plot_name='plot5', plot_title='второй график')
        self.plot5.setFixedSize(450, 320)
        self.vbox2.addWidget(self.plot5)
        self.vbox2.addStretch()

        self.plot6 = self.build_plot_item(plot_name='plot6', plot_title='Ковариация')
        self.plot6.setFixedSize(450, 320)
        self.vbox3.addWidget(self.plot6)
        self.vbox3.addStretch()

        self.hbox.addStretch()
        # self.vbox1.addWidget(self.plot4)

        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#values{background-color: rgba(240,240,240,255); padding: 0px;}''')

    def build_plot_item(self, **kwargs) -> QWidget:
        widget = QWidget()
        vbox = SelfVLayout()
        widget.setLayout(vbox)
        self.plots[kwargs['plot_name']] = pg.PlotWidget()
        self.plots[kwargs['plot_name']].setBackground('w')
        self.plots[kwargs['plot_name']].setObjectName(kwargs['plot_name'])
        title = QLabel(kwargs['plot_title'])
        title.setFixedHeight(30)
        vbox.addWidget(self.plots[kwargs['plot_name']], stretch=9)
        vbox.addWidget(title, stretch=1)
        return widget
