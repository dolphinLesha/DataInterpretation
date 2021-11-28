import math
import random
import time

import numpy as np

from src.control.filters import Filter


class Function:
    data_x = []
    data = []
    title: str = ''

    def __init__(self, **kwargs):
        # if data := kwargs.pop('data', None):
        #     self.data = data
        # if data_x := kwargs.pop('data_x', None):
        #     self.data_x = data_x
        # self.title = ''
        # if kwargs.get('title'):
        #     self.title = kwargs.get('title')
        if kwargs.get('dt'):
            self.dt = kwargs['dt']
        self.data = kwargs.get('data')
        self.data_x = kwargs.get('data_x')

    # @abstractmethod
    def build(self, **kwargs):
        self.title = ''
        if kwargs.get('title'):
            self.title = kwargs.get('title')

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
            data_new[pos[i]] = np.random.random() * (val + d - (val - d)) + (val - d) * sign[i]
        return Function(data=data_new, data_x=data_x_new)

    def return_mo(self, **kwargs):
        data_new = []
        data_x_new = []
        # avg = np.average(self.data)
        mx = np.max(self.data)
        mn = np.min(self.data)
        avg = (mx - mn) / 2 + mn
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
        for i in range(1, len(self.data) - 1):
            temp = (self.data[i - 1] + self.data[i + 1]) / 2.0 if abs(self.data[i] / self.data[i - 1]) > 50 else \
                self.data[i]
            data_new[i] = temp
        return Function(data=data_new, data_x=data_x_new)

    def anti_trend(self, **kwargs):
        data_new = []
        data_new2 = []
        data_x_new = []

        # L = int(len(self.data) * 0.02)
        # m = 1
        #
        # N = len(self.data)
        # for i in range(N//m):
        #     data_new.append(self.data[i] - np.average(self.data[i*m:i*m+L]))
        #     # data_new.append(np.average(self.data[i * m:i * m + L]))
        #     data_x_new.append(i*m)
        # for i in range(N//m, 0, -1):
        #     print(i*m-L)
        #     print(i*m)
        #     # data_new.append(self.data[i] - np.average(self.data[i*m:i*m+L]))
        #     if i*m-L < 0:
        #         break
        #     data_new2.append(np.average(self.data[i * m-L:i * m]))
        #     data_x_new.append(i*m)

        L = int(len(self.data) * 0.04)
        m = L // 2

        N = len(self.data)
        temp = np.average(self.data[0:L])
        for i in range(m + 1):
            # data_new.append(self.data[i]-temp)
            data_new.append(temp)
            data_x_new.append(i)
        for i in range(1, N // L):
            # print(f'{i=}')
            # print(f'{i*L=}')
            # print(f'{i*L+m=}')
            # print(f'{i*L+L=}')
            temp2 = np.average(self.data[i * L:i * L + L])
            k = (temp2 - temp) / (i * L + m + 1 - ((i - 1) * L + m + 1))
            b = temp - k * ((i - 1) * L + m + 1)
            for e in range((i - 1) * L + m + 1, i * L + m + 1):
                # data_new.append(self.data[e]-(e*k+b))
                data_new.append((e * k + b))
                data_x_new.append(e)
            temp = temp2

        k = (self.data[N - 1] - temp) / (N - (N - m + 1))
        b = temp - k * (N - m + 1)
        for i in range(N - m + 1, N):
            # data_new.append(self.data[i]-(i * k + b))
            data_new.append((i * k + b))
            data_x_new.append(i)

        return Function(data=data_new, data_x=data_x_new)

    def add_function(self, **kwargs):
        data_new = self.data[:]
        data_x_new = self.data_x[:]

        temp_func = kwargs['func']

        data_new = np.add(data_new, temp_func.data) / 2

        return Function(data=list(data_new), data_x=data_x_new)

    def add_random_opti(self, **kwargs):
        data_new = self.data[:]
        data_x_new = self.data_x[:]
        n = len(self.data)

        amount = kwargs['amount']
        max_p = kwargs['max_p']
        min_p = kwargs['min_p']

        for i in range(amount):
            temp_func = np.random.random(size=n) * (max_p - min_p) + min_p
            data_new = np.add(data_new, temp_func)
        data_new /= (amount + 1)

        return Function(data=list(data_new), data_x=data_x_new)

    def add_random_opti_sigma(self, **kwargs):
        data_new = self.data[:]
        data_x_new = self.data_x[:]
        n = len(self.data)

        amount = kwargs['amount']
        max_p = kwargs['max_p']
        min_p = kwargs['min_p']
        print('aaa')
        print(amount)
        for i in range(amount):
            temp_func = np.random.random(size=n) * (max_p - min_p) + min_p
            data_new = np.add(data_new, temp_func)
            # data_new /= 2 if amount > 0 else 1
            yield np.std(data_new / (i + 1))

    def remove_noise_opt(self, **kwargs):
        data_new = self.data[:]
        data_x_new = self.data_x[:]
        n = len(self.data)
        amount = kwargs['amount']
        min_p = kwargs['min_p']
        max_p = kwargs['max_p']

        a1 = kwargs['a1']
        f1 = kwargs['f1']
        dt = kwargs['dt']

        for i in range(amount):
            temp_func = (np.random.random(size=n) * (max_p - min_p) + min_p) + a1 * np.sin(
                2 * np.pi * f1 * np.array(range(n)) * dt)
            data_new = np.add(data_new, temp_func)
        data_new /= (amount + 1)

        return Function(data=list(data_new), data_x=data_x_new)

    def fourier_transform(self):
        N = len(self.data)
        data_new = self.data[:N // 2]
        data_x_new = np.array(range(N // 2))

        for n in range(N // 2):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))

    def forward_fourier(self):
        N = len(self.data)
        data_new = self.data[:N // 2]
        data_x_new = np.array(range(N // 2))

        for n in range(N // 2):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * np.exp((-1j * math.pi * n * k)/N)
                # im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            # re /= N
            # im /= N
            data_new[n] = re

        return Function(data=list(data_new), data_x=list(data_x_new))

    def back_fourier(self):
        N = len(self.data)
        data_new = self.data[:N // 2]
        data_x_new = np.array(range(N // 2))

        for n in range(N // 2):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * np.exp((1j * math.pi * n * k)/N)
                # im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            # re /= N
            # im /= N
            data_new[n] = re

        return Function(data=list(data_new), data_x=list(data_x_new))

    def multiply(self, n: int):
        ar = np.array(self.data) * n
        self.data = list(ar)

    def fourier_re_transform(self):
        N = len(self.data)
        data_new = self.data[:N // 2]
        data_x_new = np.array(range(N // 2))

        for n in range(N // 2):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))

    def fourier_transform_window(self, window: float):
        N = len(self.data)
        wd = int((N - N * window) // 2)

        data_new_orig = self.data.copy()

        for i in range(wd):
            data_new_orig[i] = 0
            data_new_orig[-i - 1] = 0

        data_new = data_new_orig[:N // 2]
        data_x_new = np.array(range(N // 2))

        for n in range(N // 2):
            re = 0
            im = 0
            for k in range(N):
                re += data_new_orig[k] * math.cos((2 * math.pi * n * k) / N)
                im += data_new_orig[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))

    def convolution(self, func: 'Function'):
        M = len(self.data)
        N = len(func.data)

        data_new = np.zeros(N)

        for k in range(N):
            sm = 0
            for j in range(M):
                sm += func.data[k - j] * self.data[j]
            data_new[k] = sm

        data_x_new = np.array(range(N))
        return Function(data=list(data_new), data_x=list(data_x_new))

    def convolution2(self, func: 'Function'):
        M = len(self.data)
        N = len(func.data)

        data_new = np.zeros(N+M)

        for k in range(N+M):
            sm = 0
            if k >= N:
                print('k>N')
                print(f'{k=}')
                print(f'{N=}')
                continue
            for j in range(M):
                print('k-j')
                print(f'{(k-j)=}')
                print(f'{k=}')
                print(f'{j=}')
                sm += func.data[(k - j) % N] * self.data[j]
            data_new[k] = sm

        data_new = data_new[M//2:-M//2]
        data_x_new = np.array(range(N))
        return Function(data=list(data_new), data_x=list(data_x_new))


class TrendLinFunc(Function):

    def build(self, **kwargs):
        super(TrendLinFunc, self).build(**kwargs)
        self.data = []
        self.data_x = []
        for i in range(kwargs['n']):
            self.data.append(kwargs['a'] * i + kwargs['b'])
            self.data_x.append(i)


class TrendExpFunc(Function):

    def build(self, **kwargs):
        super(TrendExpFunc, self).build(**kwargs)
        self.data = []
        self.data_x = []
        for i in range(kwargs['n']):
            self.data.append(np.exp(-kwargs['a'] * i) * kwargs['b'])
            self.data_x.append(i)


class RandomFunc(Function):

    def build(self, **kwargs):
        super(RandomFunc, self).build(**kwargs)
        self.data = []
        self.data_x = []
        self.data = np.random.random(size=kwargs['n']) * (kwargs['max_p'] - kwargs['min_p']) + kwargs['min_p']
        self.data_x = np.array(range(kwargs['n']))
        # for i in range(kwargs['n']):
        #     self.data.append(np.random.random() * (kwargs['max_p'] - kwargs['min_p']) + kwargs['min_p'])
        #     self.data_x.append(i)


class RandomAddFunc(Function):

    def build(self, **kwargs):
        super(RandomAddFunc, self).build(**kwargs)
        self.data = []
        self.data_x = []
        self.data = np.random.random(size=kwargs['n']) * (kwargs['max_p'] - kwargs['min_p']) + kwargs['min_p']
        self.data_x = np.array(range(kwargs['n']))

        temp = self.add_random_opti(**kwargs)
        print(np.std(temp.data))
        self.data = temp.data
        self.data_x = temp.data_x


class RandomAddSigmaFunc(Function):

    def build(self, **kwargs):
        super(RandomAddSigmaFunc, self).build(**kwargs)
        self.data = []
        self.data_x = []
        self.data = np.random.random(size=kwargs['n']) * (kwargs['max_p'] - kwargs['min_p']) + kwargs['min_p']

        data_new = []
        print('aaa1')
        kwargs.pop('amount')
        kwargs['amount'] = 1000
        self.data_x = np.array(range(kwargs['amount'] + 1))
        sigm = np.std(self.data)
        data_new.append(sigm / sigm)
        for i in self.add_random_opti_sigma(**kwargs):
            data_new.append(i / sigm)
        self.data = data_new


class RandomOwnFunc(Function):

    def build(self, **kwargs):
        super(RandomOwnFunc, self).build(**kwargs)
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
        super(AddFunction, self).build(**kwargs)
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
                    data1[e] = data1[e] + funcs[i].data[e]
            self.data.append(data1[e])
            self.data_x.append(e)


class MultiplyFunction(Function):

    def build(self, **kwargs):
        super(MultiplyFunction, self).build(**kwargs)
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
        super(HarmonicFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        n = kwargs['n']
        a1 = kwargs['a1']
        f1 = kwargs['f1']
        self.dt = kwargs['dt']
        # for i in range(n):
        #     value = a1 * np.sin(2*np.pi*f1*i*dt)
        #     self.data.append(value)
        #     self.data_x.append(i*dt)
        self.data = a1 * np.sin(2 * np.pi * f1 * np.array(range(n)) * self.dt)
        self.data_x = self.dt * np.array(range(n))

    def fourier_transform(self):
        N = len(self.data)
        # print(f'{self.dt=}')
        fgr = int(1 / (self.dt * 2))
        df = (2 * fgr) / N
        # print(f'{df=}')
        data_new = self.data.copy()[:int(fgr / df)]
        data_x_new = df * np.array(range(int(fgr / df)))
        # print(f'{data_x_new=}')

        for n in range(int(fgr / df)):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))


class HarmonicRandFunction(Function):

    def build(self, **kwargs):
        super(HarmonicRandFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        n = kwargs['n']
        a1 = kwargs['a1']
        f1 = kwargs['f1']
        dt = kwargs['dt']
        min_p = kwargs['min_p']
        max_p = kwargs['max_p']
        # for i in range(n):
        #     value = a1 * np.sin(2*np.pi*f1*i*dt)
        #     self.data.append(value)
        #     self.data_x.append(i*dt)
        self.data = a1 * np.sin(2 * np.pi * f1 * np.array(range(n)) * dt) + (
                np.random.random(size=n) * (max_p - min_p) + min_p)
        self.data_x = dt * np.array(range(n))


class HarmonicRandAddFunction(Function):

    def build(self, **kwargs):
        super(HarmonicRandAddFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        n = kwargs['n']
        a1 = kwargs['a1']
        f1 = kwargs['f1']
        dt = kwargs['dt']
        min_p = kwargs['min_p']
        max_p = kwargs['max_p']
        self.data = a1 * np.sin(2 * np.pi * f1 * np.array(range(n)) * dt) + (
                np.random.random(size=n) * (max_p - min_p) + min_p)

        self.data_x = dt * np.array(range(n))

        temp = self.remove_noise_opt(**kwargs)
        self.data = temp.data
        self.data_x = temp.data_x


class PolyHarmonicFunction(Function):

    def build(self, **kwargs):
        super(PolyHarmonicFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        n = kwargs['n']
        a1 = kwargs['a1']
        f1 = kwargs['f1']
        a2 = kwargs['a2']
        f2 = kwargs['f2']
        a3 = kwargs['a3']
        f3 = kwargs['f3']
        self.dt = kwargs['dt']
        for i in range(n):
            value1 = a1 * np.sin(2 * np.pi * f1 * i * self.dt)
            value2 = a2 * np.sin(2 * np.pi * f2 * i * self.dt)
            value3 = a3 * np.sin(2 * np.pi * f3 * i * self.dt)
            self.data.append(value1 + value2 + value3)
            self.data_x.append(i * self.dt)

    def fourier_transform(self):
        N = len(self.data)
        print(f'{self.dt=}')
        fgr = int(1 / (self.dt * 2))
        print('ln')
        print(fgr)

        df = (2 * fgr) / N
        print(f'{df=}')
        data_new = self.data.copy()[:int(fgr / df)]
        data_x_new = df * np.array(range(int(fgr / df)))

        for n in range(int(fgr / df)):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)
            # print(f'n {n}, d {data_new[n]}')

        return Function(data=list(data_new), data_x=list(data_x_new))


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
        super(SpikesFunc, self).build(**kwargs)
        func: Function = kwargs['func']
        self.data = func.data
        self.data_x = func.data_x
        C = kwargs['C']

        for i in range(self.data.__len__()):
            self.data[i] += C


class RythmFunction(Function):
    def build(self, **kwargs):
        super(RythmFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        n = kwargs['n']
        a1 = kwargs['a1']
        f1 = kwargs['f1']
        self.dt = kwargs['dt']
        self.data = np.sin(2 * np.pi * f1 * np.array(range(n)) * self.dt) * np.exp(-a1 * np.array(range(n)) * self.dt)
        mx = np.max(self.data)
        self.data /= mx
        self.data_x = self.dt * np.array(range(n))


class ImpulseReactionLPFFunction(Function):
    def build(self, **kwargs):
        super(ImpulseReactionLPFFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        m: int = kwargs['m']
        fc: float = kwargs['fc']
        self.dt: float = kwargs['dt']

        d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
        # rectangular part weights
        fact = 2 * fc * self.dt
        self.data.append(fact)
        arg = fact * math.pi
        self.data = np.sin(arg * np.array(range(1, m + 1))) / np.array(np.array(range(1, m + 1)) * math.pi)
        self.data = list(self.data)
        self.data.insert(0, fact)

        # trapezoid smoothing in the end
        self.data[m] /= 2.
        #
        # # P310 smoothing window
        sumg = self.data[0]
        for i in range(1, m + 1):
            sum = d[0]
            arg = math.pi * i / m
            for k in range(1, 4):
                sum += 2. * d[k] * np.cos(arg * k)
            self.data[i] *= sum
            sumg += 2 * self.data[i]

        for i in range(m + 1):
            self.data[i] /= sumg

        self.data_x = list(np.array(range(m + 1)))

    def fourier_transform(self):
        N = len(self.data)
        # print(f'{self.dt=}')
        fgr = int(1 / (self.dt * 2))
        df = (2 * fgr) / N
        # print(f'{df=}')
        data_new = self.data.copy()[:int(fgr / df)]
        data_x_new = df * np.array(range(int(fgr / df)))
        # print(f'{data_x_new=}')

        for n in range(int(fgr / df)):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))


class ImpulseReactionLPFSymmetricFunction(Function):
    def build(self, **kwargs):
        super(ImpulseReactionLPFSymmetricFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        m: int = kwargs['m']
        fc: float = kwargs['fc']
        self.dt: float = kwargs['dt']

        self.data = Filter.lpf(fc, self.dt, m)

        self.data_x = list(np.array(range(-m, m + 1)))

    def fourier_transform(self):
        N = len(self.data)
        # print(f'{self.dt=}')
        fgr = int(1 / (self.dt * 2))
        df = (2 * fgr) / N
        # print(f'{df=}')
        data_new = self.data.copy()[:int(fgr / df)]
        data_x_new = df * np.array(range(int(fgr / df)))
        # print(f'{data_x_new=}')

        for n in range(int(fgr / df)):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))


class ImpulseReactionHPFSymmetricFunction(Function):
    def build(self, **kwargs):
        super(ImpulseReactionHPFSymmetricFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        m: int = kwargs['m']
        fc: float = kwargs['fc']
        self.dt: float = kwargs['dt']

        self.data = Filter.hpf(fc, self.dt, m)

        self.data_x = list(np.array(range(-m, m + 1)))

    def fourier_transform(self):
        N = len(self.data)
        # print(f'{self.dt=}')
        fgr = int(1 / (self.dt * 2))
        df = (2 * fgr) / N
        # print(f'{df=}')
        data_new = self.data.copy()[:int(fgr / df)]
        data_x_new = df * np.array(range(int(fgr / df)))
        # print(f'{data_x_new=}')

        for n in range(int(fgr / df)):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))


class ImpulseReactionBPFSymmetricFunction(Function):
    def build(self, **kwargs):
        super(ImpulseReactionBPFSymmetricFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        m: int = kwargs['m']
        fc1: float = kwargs['fc1']
        fc2: float = kwargs['fc2']
        self.dt: float = kwargs['dt']

        self.data = Filter.bpf(fc1, fc2, self.dt, m)

        self.data_x = list(np.array(range(-m, m + 1)))

    def fourier_transform(self):
        N = len(self.data)
        # print(f'{self.dt=}')
        fgr = int(1 / (self.dt * 2))
        df = (2 * fgr) / N
        # print(f'{df=}')
        data_new = self.data.copy()[:int(fgr / df)]
        data_x_new = df * np.array(range(int(fgr / df)))
        # print(f'{data_x_new=}')

        for n in range(int(fgr / df)):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))


class ImpulseReactionBSFSymmetricFunction(Function):
    def build(self, **kwargs):
        super(ImpulseReactionBSFSymmetricFunction, self).build(**kwargs)
        self.data = []
        self.data_x = []
        m: int = kwargs['m']
        fc1: float = kwargs['fc1']
        fc2: float = kwargs['fc2']
        self.dt: float = kwargs['dt']

        self.data = Filter.bsf(fc1, fc2, self.dt, m)

        self.data_x = list(np.array(range(-m, m + 1)))

    def fourier_transform(self):
        N = len(self.data)
        # print(f'{self.dt=}')
        fgr = int(1 / (self.dt * 2))
        df = (2 * fgr) / N
        # print(f'{df=}')
        data_new = self.data.copy()[:int(fgr / df)]
        data_x_new = df * np.array(range(int(fgr / df)))
        # print(f'{data_x_new=}')

        for n in range(int(fgr / df)):
            re = 0
            im = 0
            for k in range(N):
                re += self.data[k] * math.cos((2 * math.pi * n * k) / N)
                im += self.data[k] * math.sin((2 * math.pi * n * k) / N)
            re /= N
            im /= N
            data_new[n] = math.sqrt(re ** 2 + im ** 2)

        return Function(data=list(data_new), data_x=list(data_x_new))
