import random
import time
from abc import abstractmethod

import numpy as np



class Function:

    data_x = []
    data = []

    def __init__(self, **kwargs):
        if data := kwargs.pop('data', None):
            self.data = data
        if data_x := kwargs.pop('data_x', None):
            self.data_x = data_x

    @abstractmethod
    def build(self, **kwargs):
            pass

    def shift(self, **kwargs) -> 'Function':
        C = kwargs['C']
        data_new = []
        data_x_new = []
        for i in range(self.data.__len__()):
            data_new.append(self.data[i] + C)
            data_x_new.append(self.data_x[i])
        return Function(data=data_new, data_x=data_x_new)

    def spikes(self, **kwargs) -> 'Function':
        n = kwargs['n']
        pos = kwargs.pop('pos', None)
        if pos is None:
            pos = []
            # for i in range(n):
            #     pos[i] = np.random.randint(0, self.data.__len__())
            pos = random.sample(range(len(self.data)), n)
        sign = kwargs.pop('sign', None)
        if sign is None:
            sign = []
            for i in range(n):
                m = np.random.randint(-1, 1)
                sign.append(m if m == -1 else 1)

        return self._spikes(n, pos, sign, kwargs['val'], kwargs['d'])

    def _spikes(self, n: int, pos: list[int], sign: list[int], val: int, d: int) -> 'Function':
        data_new = list(self.data)
        data_x_new = list(self.data_x)
        for i in range(n):
            data_new[pos[i]] = np.random.random() * (val + d - (val-d)) + (val-d) * sign[i]
        return Function(data=data_new, data_x=data_x_new)

    def return_mo(self, **kwargs):
        data_new = []
        data_x_new = []
        avg = np.average(self.data)
        return self.shift(**{'C': -avg})

    # def anti_spikes(self, **kwargs):
    #     data_new = []
    #     data_x_new = []
    #     q1 = np.quantile(self.data, 0.25)
    #     q2 = np.quantile(self.data, 0.5)
    #     q3 = np.quantile(self.data, 0.75)
    #     q13 = q3-q1
    #     q13 *= 3.0
    #     q1s = q1 - q13
    #     q3s = q3 + q13
    #     data_new.append(self.data[0])
    #     data_x_new.append(self.data_x[0])
    #     # mn = np.mean(self.data)
    #     for i in range(1, len(self.data)-1):
    #         temp = 0.
    #         if self.data[i] < q1s or self.data[i] > q3s:
    #             # temp = (self.data[i-1] + self.data[i+1] + self.data[i-2] + self.data[i+2] + mn) / 5.0
    #             temp = (self.data[i - 1] + self.data[i + 1]) / 2.0
    #             # temp = mn
    #         else:
    #             temp = (self.data[i])
    #         data_new.append(temp)
    #         data_x_new.append(self.data_x[i])
    #     data_new.append(self.data[len(self.data)-1])
    #     data_x_new.append(self.data_x[len(self.data)-1])
    #     return Function(data=data_new, data_x=data_x_new)

    def anti_spikes(self, **kwargs):
        data_new = self.data[:]
        data_x_new = self.data_x[:]
        for i in range(1, len(self.data)-1):
            temp = (self.data[i - 1] + self.data[i + 1]) / 2.0 if abs(self.data[i]/self.data[i-1]) > 50 else self.data[i]
            data_new[i] = temp
        return Function(data=data_new, data_x=data_x_new)


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


class HarmonicFunction(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        n = kwargs['n']
        a1 = kwargs['a1']
        f1 = kwargs['f1']
        dt = kwargs['dt']
        for i in range(n):
            value = a1 * np.sin(2*np.pi*f1*i*dt)
            self.data.append(value)
            self.data_x.append(i*dt)


class PolyHarmonicFunction(Function):

    def build(self, **kwargs):
        self.data = []
        self.data_x = []
        n = kwargs['n']
        a1 = kwargs['a1']
        f1 = kwargs['f1']
        a2 = kwargs['a2']
        f2 = kwargs['f2']
        a3 = kwargs['a3']
        f3 = kwargs['f3']
        dt = kwargs['dt']
        for i in range(n):
            value1 = a1 * np.sin(2*np.pi*f1*i*dt)
            value2 = a2 * np.sin(2*np.pi*f2*i*dt)
            value3 = a3 * np.sin(2*np.pi*f3*i*dt)
            self.data.append(value1+value2+value3)
            self.data_x.append(i*dt)


# class ShiftFunc(Function):
#     def build(self, **kwargs):
#         func: Function = kwargs['func']
#         self.data = func.data
#         self.data_x = func.data_x
#         C = kwargs['C']
#
#         for i in range(self.data.__len__()):
#             self.data[i] += C


class SpikesFunc(Function):
    def build(self, **kwargs):
        func: Function = kwargs['func']
        self.data = func.data
        self.data_x = func.data_x
        C = kwargs['C']

        for i in range(self.data.__len__()):
            self.data[i] += C