import random
import time
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


class RandomFunc(Function, FunctionMixin):

    def build(self, n: int, min_p: float, max_p: float, **kwargs):
        self.data = []
        for i in range(n):
            self.data.append(random.random() * (max_p - min_p) + min_p)


class RandomOwnFunc(Function, FunctionMixin):

    def build(self, n: int, min_p: float, max_p: float, precision: int = 1000, **kwargs):
        self.data = []
        sec = round(time.time() * 1000)
        proc = (sec) % precision
        for i in range(n):
            # proc = (pi+sec) % precision
            if 0 <= proc % 10 < 3:
                a = (proc * 9312) ** 2 / 100
                b = (proc * 12) ** 5 / 12.5
            elif 3 <= proc % 10 < 6:
                a = (proc * 4562) ** 4 / 456
                b = (proc * 312) ** 2 / 123.5
            else:
                a = (proc * 1234) ** 2 / 123
                b = (proc * 876) ** 7 / 432
            if a < b:
                a = b
            stri = str(a)[0:6].replace('.', '')
            a = int(stri)
            proc = int(a % precision)
            self.data.append((proc / precision) * (max_p - min_p) + min_p)
