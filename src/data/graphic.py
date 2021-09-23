import time
from enum import Enum

import numpy
import numpy as np
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

from src.control.function import Function


class GraphicPrefab:
    pen: pg.mkPen(color=(0, 0, 0))

    @classmethod
    def prefab_simple(cls):
        cls.pen = pg.mkPen(color=(0, 0, 0), width=2)
        return cls

    @classmethod
    def prefab_simple_thin(cls):
        cls.pen = pg.mkPen(color=(0, 0, 0), width=1)
        return cls


class Graphic:

    instance: pg.PlotWidget
    func: Function

    def __init__(self, plot_widget: pg.PlotWidget):
        self.instance = plot_widget

    def build(self, func: Function, prefab: GraphicPrefab):
        self.instance.getPlotItem().clear()
        self.instance.getPlotItem().plot(func.data, pen=prefab.pen)
        self.instance.getPlotItem().showGrid(x=True, y=True, alpha=0.2)

