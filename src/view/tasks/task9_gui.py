from PyQt5.QtCore import QSize

from src.control.analysis import AnalysisBuilder
from src.data.graphic import *
from src.view.own_widgets import *
from src.view.view_settings import ViewSettings


class WidgetTask9(QWidget):

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
        self.view_control.setFixedWidth(ViewSettings.control_width)
        self.view_control.graph_build_b.clicked.connect(self.build_graph)
        self.view_control.fourier_build_b.clicked.connect(self.build_fourier)
        self.view_control.conv_build_b.clicked.connect(self.build_convolution)
        self.main_h_box.addWidget(self.view_control)
        self.main_h_box.addWidget(self.view_graphics)

    def init_style_sheet(self):
        # self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
        #         background-color:rgba(255,255,255,255)''')
        self.view_control.setStyleSheet('''QWidget{background-color: rgb(150,150,150);}''')

    def build_graph(self):
        sender = self.sender()

        self.func = self.view_control.graph_and_settings.get_function()
        self.func2 = self.view_control.graph_and_settings2.get_function()
        Graphic(self.view_graphics.plots["plot1"]).build(func=self.func, prefab=GraphicPrefab.prefab_simple_thin())
        Graphic(self.view_graphics.plots["plot4"]).build(func=self.func2,
                                                         prefab=GraphicPrefab.prefab_simple_thin())
        # self.spiked_func = self.func2.spikes(**self.view_control.spikes_settings.get_values())
        # Graphic(self.view_graphics.plots["plot3"]).build(func=self.spiked_func,
        #                                                  prefab=GraphicPrefab.prefab_simple_thin())

    def build_fourier(self):
        sender = self.sender()

        # self.func2 = self.func.spikes(**{'n': 1})

        self.fourier = self.func.fourier_transform()

        self.fourier2 = self.func2.fourier_transform()
        # self.refourier = self.fourier.fourier_re_transform()
        if hasattr(self, 'conv1'):
            print('tut1')
            self.fourier3 = self.conv1.fourier_transform()
        # self.fourier.multiply(len(self.func.data))
        Graphic(self.view_graphics.plots["plot2"]).build(func=self.fourier,
                                                         prefab=GraphicPrefab.prefab_simple_thin())

        Graphic(self.view_graphics.plots["plot5"]).build(func=self.fourier2,
                                                         prefab=GraphicPrefab.prefab_simple_thin())
        # self.ff = self.func.forward_fourier()
        # print(self.ff.data)
        # Graphic(self.view_graphics.plots["plot3"]).build(func=self.ff,
        #                                                  prefab=GraphicPrefab.prefab_simple_thin())

        if hasattr(self, 'fourier3'):
            print('tut2')
            Graphic(self.view_graphics.plots["plot8"]).build(func=self.fourier3,
                                                             prefab=GraphicPrefab.prefab_simple_thin())

    def build_convolution(self):
        sender = self.sender()

        # self.func2 = self.func.spikes(**{'n': 1})

        self.conv1 = self.func.convolution(self.func2)
        Graphic(self.view_graphics.plots["plot7"]).build(func=self.conv1, prefab=GraphicPrefab.prefab_simple_thin())


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
        self.area = SelfControlPanel()
        self.graph_build_b = SelfButton("Построить график")
        self.fourier_build_b = SelfButton("Построить преобразование")
        self.conv_build_b = SelfButton("Построить свертку")

        '''group box for values of 1 graph'''
        group1 = QGroupBox("Функция")
        self.box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(self.box_group1)
        self.graph_and_settings = SelfFunctionCreateVariant()
        self.box_group1.addWidget(self.graph_and_settings)

        '''group box for values of 2 graph'''
        group2 = QGroupBox("Функция 2")
        self.box_group2 = SelfVLayout(spacing=5)
        group2.setLayout(self.box_group2)
        self.graph_and_settings2 = SelfFunctionCreateVariant()
        self.box_group2.addWidget(self.graph_and_settings2)

        # self.area.add_widget(self.graph_build_b)
        # self.area.add_widget(self.fourier_build_b)
        # self.area.add_widget(self.conv_build_b)
        self.area.add_widget(group1)
        self.area.add_widget(group2)
        # self.area.add_widget(group3)
        # self.area.add_widget(self.convolute)
        self.box.addWidget(self.graph_build_b)
        self.box.addWidget(self.fourier_build_b)
        self.box.addWidget(self.conv_build_b)
        self.box.addWidget(self.area)
        # self.box.addWidget(self.graph_build_b)
        # self.box.addWidget(group1)
        # self.box.addWidget(self.fourie_build_b)
        # self.box.addWidget(self.fourie_window_build_b)
        # self.box.addWidget(self.window_input)
        # self.box.addWidget(group2)
        # self.box.addStretch(1)
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
        self.plot1 = self.build_plot_item(plot_name='plot1', plot_title='График импульса')
        self.plot2 = self.build_plot_item(plot_name='plot2', plot_title='Спектр')
        self.plot3 = self.build_plot_item(plot_name='plot3', plot_title='Свертка')
        self.plot4 = self.build_plot_item(plot_name='plot4', plot_title='График функции')
        self.plot5 = self.build_plot_item(plot_name='plot5', plot_title='Спектр')
        self.plot6 = self.build_plot_item(plot_name='plot6', plot_title='Спектр')
        self.plot7 = self.build_plot_item(plot_name='plot7', plot_title='Свертка')
        self.plot8 = self.build_plot_item(plot_name='plot8', plot_title='Спектр')
        self.plot9 = self.build_plot_item(plot_name='plot9', plot_title='График с дисперсией')

        wid = 400
        hei = 250
        self.plot1.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot1)
        self.plot4.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot4)
        self.plot7.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot7)
        self.vbox1.addStretch()

        self.plot2.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot2)
        self.plot5.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot5)
        self.plot8.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot8)
        self.vbox2.addStretch()

        # self.plot3.setFixedSize(wid, hei)
        # self.vbox3.addWidget(self.plot3)
        # self.plot6.setFixedSize(wid, hei)
        # self.vbox3.addWidget(self.plot6)
        # self.plot9.setFixedSize(wid, hei)
        # self.vbox3.addWidget(self.plot9)
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
