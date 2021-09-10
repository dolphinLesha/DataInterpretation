from abc import abstractmethod

import numpy as np


class Function:

    data = []


class FunctionMixin:

    @abstractmethod
    def build(self, **kwargs):
        pass


class TrendLinFunc(Function, FunctionMixin):

    def build(self, n: int, a: float, b: float, **kwargs):
        self.data = []
        for i in range(n):
            self.data.append(a * i + b)


class TrendExpFunc(Function, FunctionMixin):

    def build(self, n: int, a: float, b: float, **kwargs):
        self.data = []
        for i in range(n):
            self.data.append(np.exp(-a * i) * b)
