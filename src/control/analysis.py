from numpy import double

from src.control.function import Function
import numpy as np


class Analysis:
    N: int = 1
    min: float
    max: float
    average: float
    var: float
    std: float
    ms: float
    rms: float
    asymmetry: float
    asymmetry_coefficient: float
    excess: float
    kurtosis: float


class AnalysisBuilder(Analysis):
    def __init__(self, func: Function):
        super(AnalysisBuilder, self).__init__()
        self.N = func.data.__len__()
        self.func_data = func.data
        self.func_data_x = func.data_x

    def average_f(self, data: list[float] = None) -> float:
        """математическое ожидание"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        # for i in range(N):
        #     sm += values[i]
        # sm /= N
        # average = sm

        average = np.mean(values)

        return average

    def variance(self, data: list[float] = None) -> float:
        """дисперсия"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        # if self.average is None:
        #     self.average(values)
        # for i in range(N):
        #     sm += (values[i] - self.average) ** 2
        # sm /= N
        # var = sm

        var = np.var(values)

        return var

    def standard_deviation(self, data: list[float] = None) -> float:
        """стандартное отклонение"""
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        # if self.var is None:
        #     self.variance(values)
        # std = np.sqrt(self.var)

        std = np.std(values)

        return std

    def ms_f(self, data: list[float] = None) -> float:
        """среднеквадратичное"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        # for i in range(N):
        #     sm += values[i] ** 2
        # ms /= N

        ms = np.average(np.square(values))

        return ms

    def rms_f(self, data: list[float] = None) -> float:
        """среднеквадратичное отклонение"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        # for i in range(N):
        #     sm += values[i] ** 2
        # sm /= N
        # rms = np.sqrt(sm)

        rms = np.sqrt(np.average(np.square(values)))

        return rms

    def asymmetry_f(self, data: list[float] = None) -> float:
        """асимметрия"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        if self.average is None:
            self.average_f()
        for i in range(self.N):
            sm += (self.func_data[i] - self.average) ** 3
        sm /= N
        asymmetry = sm

        return asymmetry

    def asymmetry_coefficient_f(self, data: list[float] = None) -> float:
        """коэфицент асимметрии"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        if self.asymmetry is None:
            self.asymmetry_f()
        if self.std is None:
            self.standard_deviation()
        asym_coef = self.asymmetry / (self.std ** 3)

        return asym_coef

    def excess_f(self, data: list[float] = None) -> float:
        """эксцесс"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        if self.average is None:
            self.average_f()
        for i in range(self.N):
            sm += (self.func_data[i] - self.average) ** 4
        sm /= N
        excess = sm

        return excess

    def kurtosis_f(self, data: list[float] = None) -> float:
        """куртозис"""
        sm: float = 0.0
        values: list[float] = self.func_data
        N: int = self.N
        if data is not None:
            values = data
            N = data.__len__()

        if self.excess is None:
            self.excess_f()
        if self.std is None:
            self.standard_deviation()
        kurtosis = self.asymmetry / (self.std ** 4) - 3

        return kurtosis

    def build_values(self):
        self.N = self.func_data.__len__()
        '''min'''
        self.min = np.min(self.func_data)
        '''max'''
        self.max = np.max(self.func_data)

        '''математическое ожидание'''
        self.average = self.average_f()

        '''дисперсия'''
        self.var = self.variance()

        self.std = self.standard_deviation()

        '''средне квадратическое'''
        self.ms = self.ms_f()

        '''средне квадратическое отклонение'''
        self.rms = self.rms_f()

        '''асимметрия'''
        self.asymmetry = self.asymmetry_f()

        '''коэфициент асимметрии'''
        self.asymmetry_coefficient = self.asymmetry_coefficient_f()

        '''эксцесс'''
        self.excess = self.excess_f()

        '''коэфициент эксцесса (куртозис)'''
        self.kurtosis = self.kurtosis_f()

    def check_stac(self, m: int, t: float) -> bool:
        self.stat_mo = []
        self.stat_D = []
        answer = True
        # 0-500 501-1000
        p = self.N // m
        for i in range(self.N // m):
            mo = self.average_f(self.func_data[i * m:i * m + m])
            D = self.variance(self.func_data[i * m:i * m + m])
            for e in range(self.stat_mo.__len__()):
                try:
                    if (self.stat_mo[e] - mo) / self.stat_mo[e] * 100 > t:
                        answer = False
                except ZeroDivisionError:
                    pass
            self.stat_mo.append(mo)
            for e in range(self.stat_D.__len__()):
                try:
                    if (self.stat_D[e] - D) / self.stat_D[e] * 100 > t:
                        answer = False
                except ZeroDivisionError:
                    pass
            self.stat_D.append(D)

        # 1001-1030
        if self.N - self.N // m * m > 0:
            mo = self.average_f(self.func_data[self.N // m * m:])
            D = self.variance(self.func_data[self.N // m * m:])
            for e in range(self.stat_mo.__len__()):
                try:
                    if (self.stat_mo[e] - mo) / self.stat_mo[e] * 100 > t:
                        answer = False
                except ZeroDivisionError:
                    pass
            self.stat_mo.append(mo)
            for e in range(self.stat_D.__len__()):
                try:
                    if (self.stat_D[e] - D) / self.stat_D[e] * 100 > t:
                        answer = False
                except ZeroDivisionError:
                    pass
            self.stat_D.append(D)

        return answer

    def probability_density(self, bars: int) -> Function:
        temp = np.histogram(self.func_data, bars)
        func: Function = Function()
        func.data = temp[0]
        func.data_x = temp[1]
        return func

    def auto_correlation_f(self) -> Function:
        data_x = []
        data = []
        self.average = self.average_f()
        for l in range(0, self.N):
            sm = 0
            sm2 = 0
            for i in range(self.N - l - 1):
                sm = sm + (self.func_data[i] - self.average) * (self.func_data[i + l] - self.average)
            for i in range(self.N - 1):
                sm2 = sm2 + (self.func_data[i] - self.average) ** 2
            data.append(sm / sm2)
            data_x.append(l)

        func: Function = Function()
        func.data = data
        func.data_x = data_x
        return func

    def auto_correlation_N_norm_f(self) -> Function:
        data_x = []
        data = []
        self.average = self.average_f()
        for l in range(0, self.N):
            sm = 0
            for i in range(self.N - l - 1):
                sm = sm + (self.func_data[i] - self.average) * (self.func_data[i + l] - self.average)
            data.append(sm / self.N)
            data_x.append(l)

        func: Function = Function()
        func.data = data
        func.data_x = data_x
        return func

    def covariance_f(self, func: Function) -> Function:
        data_x = []
        data = []
        self.average = self.average_f()

        avg2 = self.average_f(func.data)

        if self.N != func.data.__len__():
            raise ValueError('Количество элементов в функциях не совпадает')

        for l in range(0, self.N):
            sm = 0
            for i in range(self.N - l - 1):
                sm = sm + (self.func_data[i] - self.average) * (func.data[i + l] - avg2)
            data.append(sm / self.N)
            data_x.append(l)

        func: Function = Function()
        func.data = data
        func.data_x = data_x
        return func

