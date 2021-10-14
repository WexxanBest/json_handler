import json
from pathlib import Path
import os


def load_from_json(filename: str):
    with open(filename, mode='r') as file:
        data = json.load(file)

    return data


def save_to_json(filename: str, data: dict):
    with open(filename, mode='w') as file:
        json.dump(data, file)


class DictHandler(dict):
    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        if kwargs:
            d.update(**kwargs)
        for k, v in d.items():
            setattr(self, k, v)
        # Class attributes
        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')) and k not in ('update', 'pop', 'load_from_json', 'save_to'):
                print(f'{k=} {getattr(self, k)=}')
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = [self.__class__(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, dict) and not isinstance(value, self.__class__):
            value = self.__class__(value)
        super().__setattr__(name, value)
        super().__setitem__(name, value)

    __setitem__ = __setattr__

    def __delattr__(self, item):
        del self[item]

    def update(self, e=None, **f):
        d = e or dict()
        d.update(f)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):
        delattr(self, k)
        return super().pop(k, d)

    @staticmethod
    def load_from_json(filename: str):
        data = load_from_json(filename)

        return DictHandler(data)

    def save_to(self, filename):
        save_to_json(filename, self)


class JsonHandler:
    def __init__(self, filename: str, data: dict = None, default_data: dict = None, auto_save=False, auto_create=True):
        if not Path(filename).exists() and auto_create:  # create file if doesn't exist and 'auto_create' = True
            if data or not default_data:
                self.__data__ = DictHandler(data) if data else DictHandler()
            else:
                self.__data__ = DictHandler(default_data)

            if auto_save:
                save_to_json(filename, self.__data__)

        elif Path(filename).exists():  # retrieve data from json file
            self.__data__ = DictHandler.load_from_json(filename)

        else:
            raise ValueError(f"File '{filename}' does not exist and it is not allowed to create it")

        self.__default_data__ = default_data
        self.__filename__ = filename
        self.__auto_save__ = auto_save

    def save(self, filename: str = None):
        if not filename:
            filename = self.__filename__

        self.__data__.save_to(filename)

    def reset_to_default(self):
        self.__data__ = DictHandler(self.__default_data__)
        if self.__auto_save__:
            self.save()

    def delete_file(self):
        os.remove(self.__filename__)

    def __getattr__(self, item):
        return getattr(self.__data__, item)

    __getitem__ = __getattr__

    def __setattr__(self, key, value):
        if key in ('__filename__', '__data__', '__auto_save__', '__default_data__'):
            super().__setattr__(key, value)
        else:
            setattr(self.__data__, key, value)
            if self.__auto_save__:
                self.save()

    __setitem__ = __setattr__

    def __delattr__(self, item):
        del self.__data__[item]
        if self.__auto_save__:
            self.save()

    __delitem__ = __delattr__

    def __str__(self):
        return str(self.__data__)

    __repr__ = __str__

    def __dict__(self):
        return dict(self.__data__)
