import os
import tempfile
import random

"""
В этои задани необходимо было реализовать 
интрефейс для работы с файдами
"""


class File:
    def __init__(self, path):
        """
        Если файла не существует
        то он создастся
        :param path:
        """
        if not os.path.exists(path):
            with open(path, 'w'):
                pass
        self.path = path

    def read(self):
        """
        Метод для чтения
        из файла
        :return:
        """
        return open(self.path, 'r').read()

    def write(self, text):
        """
        Метод для записи
        переданного значения text
        :param text:
        :return:
        """
        with open(self.path, 'w') as f:
            f.write(text)

    def __add__(self, obj):
        """
        При сложении двух объектов типа File
        создастся новый файд и в него запишутся
        данные из обоих файлов
        :param obj:
        :return:
        """
        file_name = "afsdfsd{}".format(random.randint(1, 100000000))
        new_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(new_path, "+w") as res:
            res.write(self.read()+obj.read())
        return File(new_path)

    def __getitem__(self, item):
        return open(self.path, 'r').readlines()[item]

    def __str__(self):
        return self.path
