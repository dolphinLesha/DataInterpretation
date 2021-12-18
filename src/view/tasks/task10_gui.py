from PyQt5.QtCore import QSize, QThread

from src.data.graphic import *
from src.view.own_widgets import *
from src.view.view_settings import ViewSettings


class FileListen(QThread):

    """Поток для прослушивания аудио, не блокирующий интерфейс"""

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


class WidgetTask10(QWidget):
    """Корень вкладки, контролирующий работу всего окна с заданием"""

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.listen_thread = FileListen()
        self.listen_thread.end_signal.connect(self.get_done_listen)
        self.audio_func = AudioFunction()
        self.init_style_sheet()

    def init_ui(self):
        vbox = SelfVLayout()
        self.setLayout(vbox)
        self.title = QLabel("Задача с аудио")
        self.title.setFixedHeight(30)
        widget = QWidget()
        vbox.addWidget(self.title)
        vbox.addWidget(widget)
        self.main_h_box = SelfHLayout(spacing=10)
        widget.setLayout(self.main_h_box)
        self.view_graphics = WidgetValues()
        self.view_control = WidgetControl()
        self.view_control.setFixedWidth(ViewSettings.control_width)
        self.view_control.build_filter.clicked.connect(self.build_graph_filter)
        self.view_control.read_audio.clicked.connect(self.build_graph_audio)
        self.view_control.avg_signal.clicked.connect(self.build_graph_average)
        self.view_control.proc_b.clicked.connect(self.build_proc)
        self.view_control.proc_r.clicked.connect(self.process_rebuild)
        self.view_control.fourier_build_b.clicked.connect(self.build_fourier)
        self.view_control.play_b.clicked.connect(self.play_file)
        self.view_control.play_proc_b.clicked.connect(self.play_file_proc)
        self.view_control.stop_b.clicked.connect(self.stop_play_file)
        self.view_control.avg_signal.setEnabled(False)

        self.view_control.save_audio.clicked.connect(self.save_function)

        self.main_h_box.addWidget(self.view_control)
        self.main_h_box.addWidget(self.view_graphics)

    def init_style_sheet(self):
        self.title.setStyleSheet('''QLabel{color: rgb(%d, %d, %d);}''' % ViewSettings.foreground_color2)
        # self.view_control.setStyleSheet('''QWidget{background-color: rgb(150,150,150);}''')

    def build_graph_audio(self):
        sender = self.sender()
        path = self.view_control.file_load.path

        wav_file = AudioModule().read(path)

        self.audio_func.build_from_wav_file(wav_file=wav_file)

        if self.audio_func.channels == 2:
            self.func_l = self.audio_func.common_channel
            self.func_r = self.audio_func.right_channel

            Graphic(self.view_graphics.plot1.plot).build(func=self.func_l,
                                                         prefab=GraphicPrefab.prefab_simple_thin_white())
            Graphic(self.view_graphics.plot2.plot).build(func=self.func_r,
                                                         prefab=GraphicPrefab.prefab_simple_thin_white())
            self.view_control.avg_signal.setEnabled(True)
            self.view_control.signal_len_l.set_text(str(len(self.func_l.data)))
            self.view_control.signal_dt_l.set_text(str(self.func_l.dt))
        else:
            self.func_a = self.audio_func.common_channel
            Graphic(self.view_graphics.plot3.plot).build(func=self.func_a,
                                                         prefab=GraphicPrefab.prefab_simple_thin_white())
            self.view_control.avg_signal.setEnabled(False)
            self.view_control.signal_len_l.set_text(str(len(self.func_a.data)))
            self.view_control.signal_dt_l.set_text(str(self.func_a.dt))

    def build_graph_average(self):
        self.func_a = self.func_l.average(self.func_r)
        Graphic(self.view_graphics.plot3.plot).build(func=self.func_a,
                                                     prefab=GraphicPrefab.prefab_simple_thin_white())

    def build_graph_filter(self):
        proc = self.view_control.proc_variants.get_proc()
        print(proc)
        # if proc == 'add_func':
        self.filter = self.view_control.proc_variants.get_function()

        Graphic(self.view_graphics.plot4.plot).build(func=self.filter,
                                                     prefab=GraphicPrefab.prefab_simple_thin_white())

    def build_fourier(self):
        sender = self.sender()

        if hasattr(self, 'func_l'):
            self.fourier_l = self.func_l.fourier_transform()
            Graphic(self.view_graphics.plot6.plot).build(func=self.fourier_l,
                                                         prefab=GraphicPrefab.prefab_simple_thin_white())

        if hasattr(self, 'func_r'):
            self.fourier_r = self.func_r.fourier_transform()
            Graphic(self.view_graphics.plot7.plot).build(func=self.fourier_r,
                                                         prefab=GraphicPrefab.prefab_simple_thin_white())

        if hasattr(self, 'func_a'):
            self.fourier_a = self.func_a.fourier_transform()
            Graphic(self.view_graphics.plot8.plot).build(func=self.fourier_a,
                                                         prefab=GraphicPrefab.prefab_simple_thin_white())

        if hasattr(self, 'filter'):
            self.fourier_filter = self.filter.fourier_transform()
            Graphic(self.view_graphics.plot9.plot).build(func=self.fourier_filter,
                                                         prefab=GraphicPrefab.prefab_simple_thin_white())

        if hasattr(self, 'proc_func'):
            self.fourier_proc_func = self.proc_func.fourier_transform()
            Graphic(self.view_graphics.plot10.plot).build(func=self.fourier_proc_func,
                                                          prefab=GraphicPrefab.prefab_simple_thin_white())

    def play_file(self):
        sender = self.sender()
        path = self.view_control.file_load.path

        self.listen_thread.init_path(path)
        self.listen_thread.start()

    def play_file_proc(self):
        sender = self.sender()
        if not hasattr(self, 'proc_func'):
            raise Exception('non function')
        wav_file = AudioFunction.build_wav_from_function(self.proc_func)

        AudioModule.play_file(wav=wav_file)

    def stop_play_file(self):
        sender = self.sender()
        print('ad')
        self.listen_thread.terminate()

    def get_done_listen(self, msg):
        print(msg)

    def save_function(self):
        if not hasattr(self, 'proc_func'):
            raise Exception('non function')
        wav_file = AudioFunction.build_wav_from_function(self.proc_func)
        path = self.view_control.save_audio.path
        AudioModule.save(path=path, wav=wav_file)

    def build_proc(self):
        proc = self.view_control.proc_variants.get_proc()
        if not hasattr(self, 'proc_func'):
            self.proc_func = self.func_a
        if proc == 'add_func':
            fc = self.view_control.proc_variants.get_function()
            self.proc_func = self.proc_func.add_function(fc)
        if proc == 'multi':
            fc = self.view_control.proc_variants.get_function()
            self.proc_func = self.proc_func.multiply_function(fc)
        if proc == 'convolve':
            fc = self.view_control.proc_variants.get_function()
            self.proc_func = self.proc_func.convolution(fc)
        if proc == 'normalize':
            # fc = self.view_control.proc_variants.get_function()
            self.proc_func = self.proc_func.normalize()
        if proc == 'rmv_white_noise':
            p = self.view_control.proc_variants.get_settings()
            self.proc_func = self.proc_func.delete_white_noise(p)

        # self.proc_func = self.proc_func.delete_white_noise()

        Graphic(self.view_graphics.plot5.plot).build(func=self.proc_func,
                                                     prefab=GraphicPrefab.prefab_simple_thin_white())

    def process_rebuild(self):
        self.proc_func = self.func_a


class WidgetControl(QWidget):
    """Виджет настроек"""

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
        self.area.setObjectName('control_area')
        self.build_filter = SelfButton2("Построить функцию")
        self.read_audio = SelfButton2("Прочитать")
        self.avg_signal = SelfButton2("Усреднить каналы")
        self.save_audio = SelfFileSavePicker("Сохранить обработку")

        self.proc_variants = SelfFuncProcessingWidget()
        self.fourier_build_b = SelfButton2("Построить спектр")
        self.proc_r = SelfButton2("Сбросить преобразование")
        self.proc_b = SelfButton2('Построить преобразование')
        self.play_b = SelfButton2("Прослушать")
        self.play_proc_b = SelfButton2("Прослушать обработку")
        self.stop_b = SelfButton2("Закончить слушать")

        self.signal_len_l = SelfTitledLabel('длина сигнала', '')
        self.signal_dt_l = SelfTitledLabel('dt сигнала', '')

        '''group box for values of 1 graph'''
        group1 = SelfGroupBox("Файл")
        group1.setObjectName('control1')
        self.box_group1 = SelfVLayout(spacing=5)
        group1.setLayout(self.box_group1)
        self.file_load = SelfFileLoad()

        self.box_group1.addWidget(self.file_load)

        #
        # '''group box for values of 2 graph'''
        # group2 = QGroupBox("Функция 2")
        # self.box_group2 = SelfVLayout(spacing=5)
        # group2.setLayout(self.box_group2)
        # self.graph_and_settings2 = SelfFunctionCreateVariant()
        # self.box_group2.addWidget(self.graph_and_settings2)

        self.area.add_widget(group1)
        # self.area.add_widget(group2)
        # self.area.add_widget(group3)

        self.box.addWidget(self.read_audio)
        self.box.addWidget(self.avg_signal)
        self.box.addWidget(self.proc_variants)
        self.box.addWidget(self.build_filter)
        self.box.addWidget(self.proc_b)
        self.box.addWidget(self.proc_r)
        self.box.addWidget(self.fourier_build_b)
        self.box.addWidget(self.save_audio)
        self.box.addWidget(self.signal_len_l)
        self.box.addWidget(self.signal_dt_l)
        self.box.addWidget(self.play_b)
        self.box.addWidget(self.play_proc_b)
        self.box.addWidget(self.stop_b)
        self.box.addWidget(self.area)
        self.init_style_sheet()

    def init_style_sheet(self):
        self.setStyleSheet('''QWidget#z2wid{background-color: rgb(%d,%d,%d);}''' % ViewSettings.background_color)
        self.area.setStyleSheet(
            '''QWidget#conrol_area{background-color: rgb(%d,%d,%d);}''' % ViewSettings.background_color)


class WidgetValues(QWidget):
    """Главное окно вкладки с заданием"""

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

        self.plot1 = SelfPlot(title='Левый канал')
        self.plot2 = SelfPlot(title='Правый канал')
        self.plot3 = SelfPlot(title='Усредненный сигнал (или единственный канал)')
        self.plot4 = SelfPlot(title='Функция')
        self.plot5 = SelfPlot(title='Результат обработки')
        self.plot6 = SelfPlot(title='Спектр')
        self.plot7 = SelfPlot(title='Спектр')
        self.plot8 = SelfPlot(title='Спектр')
        self.plot9 = SelfPlot(title='Спектр')
        self.plot10 = SelfPlot(title='Спектр')

        wid = 600
        hei = 150
        self.plot1.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot1)
        self.plot2.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot2)
        self.plot3.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot3)
        self.plot4.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot4)
        self.plot5.setFixedSize(wid, hei)
        self.vbox1.addWidget(self.plot5)
        self.vbox1.addStretch()

        self.plot6.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot6)
        self.plot7.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot7)
        self.plot8.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot8)
        self.plot9.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot9)
        self.plot10.setFixedSize(wid, hei)
        self.vbox2.addWidget(self.plot10)
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
