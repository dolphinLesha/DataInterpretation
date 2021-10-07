import random
import time
from abc import abstractmethod

import numpy as np


class Function:

    data_x = []
    data = []

    @abstractmethod
    def build(self, **kwargs):
            pass


# class FunctionMixin:
#
#     @abstractmethod
#     def build(self, **kwargs):
#         pass


class TrendLinFunc(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        for i in range(kwargs['n']):
            self.data.append(kwargs['a'] * i + kwargs['b'])
            self.data_x.append(i)


class TrendExpFunc(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        for i in range(kwargs['n']):
            self.data.append(np.exp(-kwargs['a'] * i) * kwargs['b'])
            self.data_x.append(i)


class SinusFunc(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        for i in range(kwargs['n']):
            self.data.append()
            self.data_x.append(i)


class RandomFunc(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        for i in range(kwargs['n']):
            self.data.append(np.random.random() * (kwargs['max_p'] - kwargs['min_p']) + kwargs['min_p'])
            self.data_x.append(i)


class RandomOwnFunc(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        sec = round(time.time() * 1000)
        proc = (sec) % kwargs['precision']
        for i in range(kwargs['n']):
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
            proc = int(a % kwargs['precision'])
            self.data.append((proc / kwargs['precision']) * (kwargs['max_p'] - kwargs['min_p']) + kwargs['min_p'])
            self.data_x.append(i)


class AddFunction(Function):

    def build(self, **kwargs):
        self.data=[]
        self.data_x = []
        funcs = kwargs['funcs']

        max_index = 0
        max_i = funcs[0].data.__len__()
        for i in range(1, funcs.__len__()):
            if funcs[i].data.__len__() > max_i:
                max_i = funcs[i].data.__len__()
                max_index = i

        data1 = funcs[max_index].data
        for e in range(data1.__len__()):
            for i in range(0, funcs.__len__()):
                if i == max_index:
                    continue
                if funcs[i].data.__len__() > e:
                    data1[e] = data1[e] + funcs[i].data[e]
            self.data.append(data1[e])
            self.data_x.append(e)


class MultiplyFunction(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        funcs = kwargs['funcs']

        max_index = 0
        max_i = funcs[0].data.__len__()
        for i in range(1, funcs.__len__()):
            if funcs[i].data.__len__() > max_i:
                max_i = funcs[i].data.__len__()
                max_index = i

        data1 = funcs[max_index].data
        for e in range(data1.__len__()):
            for i in range(0, funcs.__len__()):
                if i == max_index:
                    continue
                if funcs[i].data.__len__() > e:
                    data1[e] = data1[e] * funcs[i].data[e]
            self.data.append(data1[e])
            self.data_x.append(e)


