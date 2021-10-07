import pyqtgraph as pg

from src.control.function import *


class GraphicPrefab:
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
    def prefab_dark_blue(cls):
        cls.pen = pg.mkPen(color=(0, 0, 30), width=2)
        cls.grid_alpha = 0.3
        return cls


class Graphic:
    instance: pg.PlotWidget
    func: Function

    def __init__(self, plot_widget: pg.PlotWidget):
        self.instance = plot_widget

    def build(self, func: Function, prefab: GraphicPrefab):
        self.instance.getPlotItem().clear()
        self.instance.getPlotItem().plot(func.data_x, func.data, pen=prefab.pen)
        self.instance.getPlotItem().showGrid(x=True, y=True, alpha=prefab.grid_alpha)

    def build_histogram(self, func: Function, prefab: GraphicPrefab):
        self.instance.getPlotItem().clear()
        self.instance.getPlotItem().plot(func.data_x, func.data, stepMode=True, fillLevel=0, brush=(0, 0, 30))
        self.instance.getPlotItem().showGrid(x=True, y=True, alpha=prefab.grid_alpha)


class FunctionVariants:
    def __init__(self):
        self.variants = {'TrendLinFunc': TrendLinFunc(), 'TrendExpFunc': TrendExpFunc(), 'RandomFunc': RandomFunc(),
                         'RandomOwnFunc': RandomOwnFunc()}


# ## make interesting distribution of values
# vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])
#
# ## compute standard histogram
# y, x = np.histogram(vals, bins=np.linspace(-3, 10, 40))
#
# ## Using stepMode=True causes the plot to draw two lines for each sample.
# ## notice that len(x) == len(y)+1
# plt1.plot(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))
