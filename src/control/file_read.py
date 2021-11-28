import binascii

import numpy as np
import struct

from src.control.function import Function, HarmonicFunction


class FileReader:
    def __init__(self, path: str):
        self.path = path

    def load_data(self):
        _, typ, n, dt = self.path.split('.')[0].split('_')
        n = int(n)
        dt = str(dt)
        digit = ''
        typ = ''
        for sym in dt:
            if sym.isdigit():
                digit += sym
            else:
                typ = dt[dt.index(sym):]
                break
        # print(digit)
        # print(typ)
        if typ == 'ms':
            digit = float(digit)/1000
        dt = float(digit)
        return self._load_data_harm_usual(n, dt)

    def _load_data_harm(self, n: int, dt: float):
        dtype = np.dtype('B')
        arr = np.fromfile(self.path, dtype=dtype, count=n, sep='')
        print(len(arr))
        data_x = dt * np.array(range(len(arr)))
        return HarmonicFunction(data_x=list(data_x), data=list(arr), dt=dt)

    def _load_data_harm_usual(self, n: int, dt: float):
        try:
            with open(self.path, "rb") as f:
                bytess = f.read()
                # print(bytess)
                # data_bytes2ascii = binascii.b2a_uu(bytess)
                # print(data_bytes2ascii)
                # while bytess:
                #     bytess = f.read(45)
                #     print(bytess)
                #     data_bytes2ascii = binascii.b2a_uu(bytess)
                #     print(data_bytes2ascii)
                # print(struct.unpack('>f', bytess))
                values = np.frombuffer(bytearray(bytess), dtype=np.float32)
                data_x = dt * np.array(range(len(values)))
                # print(len(values))
                return HarmonicFunction(data_x=list(data_x), data=list(values), dt=dt)

        except IOError:
            print('Error While Opening the file!')
