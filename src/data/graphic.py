import pyqtgraph as pg

from src.control.function import *
from src.view.view_settings import ViewSettings


class GraphicPrefab:
    """
    Префабы настроек графиков
    """
    pen: pg.mkPen(color=(0, 0, 0))
    grid_alpha = 0.2

    @classmethod
    def prefab_simple(cls):
        cls.pen = pg.mkPen(color=(0, 0, 0), width=2)
        return cls

    @classmethod
    def prefab_simple_thin(cls):
        cls.pen = pg.mkPen(color=(0, 0, 0), width=1)
        return cls

    @classmethod
    def prefab_simple_thin_white(cls):
        cls.pen = pg.mkPen(color=(int('%d' % ViewSettings.foreground_color[0]),
                                  int('%d' % ViewSettings.foreground_color[1]),
                                  int('%d' % ViewSettings.foreground_color[2])), width=1)
        cls.grid_alpha = 0.5
        return cls

    @classmethod
    def prefab_dark_blue(cls):
        cls.pen = pg.mkPen(color=(0, 0, 30), width=2)
        cls.grid_alpha = 0.3
        return cls


class Graphic:
    """
    Класс, позволяющий строить функции на графике

    В виде тренда или гистрограммы
    """
    instance: pg.PlotWidget
    func: Function

    def __init__(self, plot_widget: pg.PlotWidget):
        self.instance = plot_widget

    def build(self, func: Function, prefab: GraphicPrefab, **kwargs):
        self.instance.getPlotItem().clear()
        if func.title is not None and func.title!='':
            self.instance.getPlotItem().setTitle(func.title)
        graph_limit = kwargs.get('graph_limit')
        if graph_limit:
            self.instance.getPlotItem().setYRange(graph_limit[0], graph_limit[1])
        if func.data_x is not None:
            self.instance.getPlotItem().plot(func.data_x, func.data, pen=prefab.pen)
        else:
            self.instance.getPlotItem().plot(func.data, pen=prefab.pen)
        self.instance.getPlotItem().showGrid(x=True, y=True, alpha=prefab.grid_alpha)

    def build_histogram(self, func: Function, prefab: GraphicPrefab, title: str = ''):
        self.instance.getPlotItem().clear()
        self.instance.getPlotItem().setTitle(title)
        self.instance.getPlotItem().plot(func.data_x, func.data, stepMode=True, fillLevel=0, brush=(0, 0, 30))
        self.instance.getPlotItem().showGrid(x=True, y=True, alpha=prefab.grid_alpha)


class Variants:
    def __init__(self):
        pass

    func_variants = {'Прямая': TrendLinFunc(),
                        'Экспонента': TrendExpFunc(),
                        'Рандом': RandomFunc(),
                        'Накопления шума': RandomAddFunc(),
                        'Свой рандом': RandomOwnFunc(),
                        'Гармоника': HarmonicFunction(),
                        'Гармоника с шумами': HarmonicRandFunction(),
                        'Гармоника с шумами (с накоплениями)': HarmonicRandAddFunction(),
                        'Полигармоника': PolyHarmonicFunction(), 'Ритм': RythmFunction(),
                        'ФНЧ': ImpulseReactionLPFFunction(),
                        'ФНЧ (сим)': ImpulseReactionLPFSymmetricFunction(),
                         'ФBЧ (сим)': ImpulseReactionHPFSymmetricFunction(),
                         'ПФ (сим)': ImpulseReactionBPFSymmetricFunction(),
                         'РФ (сим)': ImpulseReactionBSFSymmetricFunction()}

    proc_variants = {'add': 'Добавить константу',
                     'add_func': 'Добавить функцию',
                     'fourier': 'Преобразование Фурье',
                     'convolve': 'Свертка',
                     'multi': 'Умножить на функцию',
                     'normalize': 'Нормализовать по максимуму',
                     'rmv_white_noise': 'Удалить белый шум'}
