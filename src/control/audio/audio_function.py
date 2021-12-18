import numpy as np

from src.control.audio.audio_module import WavFile
from src.control.function import Function


class AudioFunction:
    """Класс, хранящий осциллограммы звукового файла, позволяющий строить wav файл из функции и преобразовывать wav файл в фунции"""
    common_channel: Function
    right_channel: Function
    channels: int

    def __init__(self):
        pass

    def build_from_wav_file(self, wav_file: WavFile):
        data = wav_file.data
        fc = wav_file.fc
        dt = 1. / fc
        x_len = data.shape[0]
        print(len(data.shape))
        if len(data.shape) == 1:
            self.channels = 1
            l_data = data
        else:
            self.channels = data.shape[1]
            l_data = np.delete(data, 1, axis=1)
            l_data.resize((x_len))

        data_x_new = list(dt * np.arange(x_len))
        data_new = list(l_data)
        self.common_channel = Function(data=data_new, data_x=data_x_new, dt=dt)

        if self.channels == 2:
            r_data = np.delete(data, 0, axis=1)
            r_data.resize((x_len))
            data_new2 = list(r_data)
            self.right_channel = Function(data=data_new2, data_x=data_x_new, dt=dt)

    def build_wav(self):
        if not hasattr(self, 'dt'):
            raise Exception('non dt')
        fc = 1. / self.common_channel.dt
        if self.channels == 2:
            array = np.asarray(np.array([self.common_channel.data, self.right_channel.data]), dtype=np.float32)
        else:
            array = np.asarray(np.array(self.common_channel.data), dtype=np.float32)
        return WavFile(array, fc)

    @staticmethod
    def build_wav_from_function(func: Function) -> WavFile:
        if not hasattr(func, 'dt'):
            raise Exception('non dt')
        fc = 1. / func.dt
        array = func.data
        if type(array) == list:
            array = np.asarray(func.data, dtype=np.float32)
        return WavFile(array, fc)

    @staticmethod
    def build_wav_from_functions(left: Function, right: Function) -> WavFile:
        if not hasattr(left, 'dt'):
            raise Exception('l non dt')
        if not hasattr(right, 'dt'):
            raise Exception('r non dt')
        if left.data.dt != right.dt:
            raise Exception('not same dt')
        if len(left.data) != len(right.data):
            raise Exception('not same len')
        fc = 1. / left.dt
        array = np.asarray(np.array([left.data, right.data]), dtype=np.float32)
        return WavFile(array, fc)
