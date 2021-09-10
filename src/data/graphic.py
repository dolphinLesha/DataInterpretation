import time

import PIL
import matplotlib.pyplot as plt
import cv2 as cv
import numpy
import numpy as np

from src.control.function import Function


class Graphic:
    _func: Function

    data: numpy.ndarray

    def __init__(self, func: Function):
        self._func = func
        fig = plt.figure()

        plt.plot(self._func.data)
        plt.show()

        nparr = np.fromstring(fig.canvas.tostring_rgb(), np.uint8).reshape(
            fig.canvas.get_width_height()[1], fig.canvas.get_width_height()[0], 3
        )
        img = cv.cvtColor(nparr.astype(np.uint8), cv.COLOR_BGR2RGB)
        self.data = img
