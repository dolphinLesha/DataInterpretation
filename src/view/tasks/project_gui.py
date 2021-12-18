from PyQt5.QtCore import QSize, QThread, pyqtSignal
from PyQt5.QtWidgets import QSizePolicy

from src.control.analysis import AnalysisBuilder
from src.control.audio.audio_module import AudioModule
from src.data.graphic import *
from src.view.own_widgets import *
from src.view.view_settings import ViewSettings


class FileListen(QThread):
    end_signal = pyqtSignal(str)
    # _send_imgs = pyqtSignal(list)
    def __init__(self):
        super(FileListen, self).__init__()

    def __del__(self):
        self.wait()

    def init_path(self, path: str):
        self.path = path

    def run(self):
        print('run')
        print(self.path)
        AudioModule().play()
        self.end_signal.emit('done')

    def terminate(self) -> None:
        AudioModule().stop()
        super(FileListen, self).terminate()

# self.thred = Thread(self.digit_model,self.save_model,self.images,self.t_otvety)
#         self.thred._signal.connect(self.get_signal)
#         self.thred._send_imgs.connect(self.get_images)
#         self.thred.start()
#
#
#         # self.show_results(rez_images)
#     def get_signal(self,msg):
#         val = (msg+1) / len(self.images)
#         val = int(val*100)
#         self.prog_bar.setValue(val)
#
#     def get_images(self, imgs):
#         self.show_results(imgs)

class WidgetProject(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.listen_thread = FileListen()
        self.listen_thread.end_signal.connect(self.get_done_listen)
        # self.init_style_sheet()

    def init_ui(self):
        vbox = SelfVLayout()
        self.setLayout(vbox)
        title = QLabel("Проект")
        title.setFixedHeight(30)
        widget = QWidget()
        vbox.addWidget(title)
        vbox.addWidget(widget)
        self.main_h_box = SelfHLayout(spacing=10)
        widget.setLayout(self.main_h_box)
        self.view_graphics = WidgetValues()
        self.view_control = WidgetControl()
        self.view_control.setFixedWidth(ViewSettings.control_width)
        self.view_control.read_audio.clicked.connect(self.build_graph_audio)
        self.view_control.fourier_build_b.clicked.connect(self.build_fourier)
        self.view_control.play_b.clicked.connect(self.play_file)
        self.view_control.stop_b.clicked.connect(self.stop_play_file)
        self.main_h_box.addWidget(self.view_control)
        self.main_h_box.addWidget(self.view_graphics)

    def init_style_sheet(self):
        # self.view_graphics.setStyleSheet('''border: 1px; padding: 0px;
        #         background-color:rgba(255,255,255,255)''')
        self.view_control.setStyleSheet('''QWidget{background-color: rgb(150,150,150);}''')

    def build_graph_audio(self):
        sender = self.sender()
        path = self.view_control.file_load.path

        data, fc = AudioModule().read(path)
        self.func_l, self.func_r = Function.build_from_wav_data_fc(data, fc)
        Graphic(self.view_graphics.plots["plot1"]).build(func=self.func_l, prefab=GraphicPrefab.prefab_simple_thin())
        Graphic(self.view_graphics.plots["plot2"]).build(func=self.func_r, prefab=GraphicPrefab.prefab_simple_thin())
        # Graphic(self.view_graphics.plots["plot4"]).build(func=self.func2,
        #                                                  prefab=GraphicPrefab.prefab_simple_thin())

    def build_fourier(self):
        sender = self.sender()

        self.fourier = self.func_l.fourier_transform()

        Graphic(self.view_graphics.plots["plot3"]).build(func=self.fourier,
                                                         prefab=GraphicPrefab.prefab_simple_thin())

    def play_file(self):
        sender = self.sender()
        path = self.view_control.file_load.path

        self.listen_thread.init_path(path)
        self.listen_thread.start()

    def stop_play_file(self):
        sender = self.sender()
        print('ad')
        self.listen_thread.terminate()

    def get_done_listen(self, msg):
        print(msg)

    def save_function(self):
        pass


class WidgetControl(QWidget):
    def __init__(self, size: QSize = None):
        super().__init__()
        if size is not None:
            self.setFixedSize(size)
        self.setObjectName("z2wid")
        self.init_ui()
        self.init_style_sheet()

    def init_ui(self):
        self.box = SelfVLayout(spacing=5)
        self.setLayout(self.box)
        self.area = SelfControlPanel()
        self.read_audio = SelfButton2("Прочитать")
        self.save_audio = SelfButton2("Сохранить обработку")
        self.fourier_build_b = SelfButton2("Построить спектр")
        self.convolve_b = SelfButton2('Построить свертку')
        self.play_b = SelfButton2("Прослушать")
        self.stop_b = SelfButton2("Заокнчить слушать")

        '''group box for values of 1 graph'''
        group1 = QGroupBox("Файл")
        self.box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(self.box_group1)
        self.file_load = SelfFileLoad()
        self.box_group1.addWidget(self.file_load)

        group2 = QGroupBox("Фильтр")
        self.box_group2 = SelfVLayout(spacing=5)
        group2.setLayout(self.box_group2)
        self.graph_variant = SelfFunctionCreateVariant()
        self.box_group2.addWidget(self.graph_variant)

        self.file_load.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,
                                                 QSizePolicy.Minimum))
        #
        # '''group box for values of 2 graph'''
        # group2 = QGroupBox("Функция 2")
        # self.box_group2 = SelfVLayout(spacing=5)
        # group2.setLayout(self.box_group2)
        # self.graph_and_settings2 = SelfFunctionCreateVariant()
        # self.box_group2.addWidget(self.graph_and_settings2)

        self.area.add_widget(group1)
        self.area.add_widget(group2)
        # self.area.add_widget(group3)

        self.box.addWidget(self.read_audio)
        self.box.addWidget(self.fourier_build_b)
        self.box.addWidget(self.convolve_b)
        self.box.addWidget(self.play_b)
        self.box.addWidget(self.stop_b)
        self.box.addWidget(self.area)
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
        self.plot1 = self.build_plot_item(plot_name='plot1', plot_title='Левый канал')
        self.plot2 = self.build_plot_item(plot_name='plot2', plot_title='Правый канал')
        self.plot3 = self.build_plot_item(plot_name='plot3', plot_title='Спектр')
        self.plot4 = self.build_plot_item(plot_name='plot4', plot_title='Фильтр')
        self.plot5 = self.build_plot_item(plot_name='plot5', plot_title='Спектр фильтра')
        # self.plot6 = self.build_plot_item(plot_name='plot6', plot_title='Спектр')
        # self.plot7 = self.build_plot_item(plot_name='plot7', plot_title='Свертка')
        # self.plot8 = self.build_plot_item(plot_name='plot8', plot_title='Спектр')
        # self.plot9 = self.build_plot_item(plot_name='plot9', plot_title='График с дисперсией')

        wid = 600
        hei = 200
        self.plot1.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot1)
        self.plot2.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot2)
        self.plot3.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot3)
        self.vbox1.addStretch()

        self.plot4.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot4)
        self.plot5.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot5)
        # self.plot8.setFixedSize(wid, hei)
        # self.vbox2.addWidget(self.plot8)
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
