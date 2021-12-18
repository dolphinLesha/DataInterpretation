import numpy as np
import sounddevice as sd
import soundfile as sf
from numpy import ndarray

from scipy.io import wavfile


class AudioModule:
    """Класс для работы с wav файлами"""

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(AudioModule, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def read(self, path: str):
        filename = path
        # Extract data and sampling rate from file
        data, fc = sf.read(filename, dtype='float32')
        self.wav_file = WavFile(data, fc)
        return self.wav_file

    @staticmethod
    def save(path: str, wav: 'WavFile'):
        wavfile.write(path, int(wav.fc), wav.data)
        print('saved')

    def play(self):
        sd.play(self.wav_file.data, self.wav_file.fc)
        # status = sd.wait()  # Wait until file is done playing
        # print(status)

    @staticmethod
    def play_file(wav: 'WavFile'):
        sd.play(wav.data, wav.fc)
        # status = sd.wait()  # Wait until file is done playing
        # print(status)

    def stop(self):
        sd.stop()


class WavFile:
    """Класс, хранящий данные wav файла"""

    def __init__(self, data: ndarray, fc):
        self.data = data
        self.fc = fc
