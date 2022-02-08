import json
from pathlib import Path
import os


def load_from_json(filename: str, encoding: str = 'utf-8'):
    with open(filename, mode='r', encoding=encoding) as file:
        data = json.load(file)

    return data


def save_to_json(filename: str, data: dict, encoding: str = 'utf-8'):
    with open(filename, mode='w', encoding=encoding) as file:
        json.dump(data, file)


class DictHandler(dict):
    """
    Class helps you handling Python dict as if it was an objects with attributes
    """
    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        if kwargs:
            d.update(**kwargs)
        for k, v in d.items():
            setattr(self, k, v)

        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')) and k not in ('update', 'pop', 'load_from_json', 'save_to'):
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
    def load_from_json(filename: str, encoding='utf-8'):
        data = load_from_json(filename, encoding=encoding)

        return DictHandler(data)

    def save_to(self, filename, encoding='utf-8'):
        save_to_json(filename, self, encoding=encoding)


class JsonHandler:
    """
    Class helps you handling JSON-like files as if it was an objects with attributes
    """
    def __init__(self, filename: str, data: dict = None, default_data: dict = None, auto_save=False, auto_create=False):
        """
        :param str filename: name of JSON-like file to handle
        :param dict data: data you can pass on initialization (default is None)
        :param dict default_data: data which will be applied if there is no data in JSON-file
        and 'data' parameter not provided (default is None)
        :param bool auto_save: if True it will save data to JSON-file each time data is changing (default is True)
        :param bool auto_create: if True file will automatically creates if it does not exist

        :raises FileNotFoundError: if there is no such filename and 'auto_create' = False
        """
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
            raise FileNotFoundError(f"File '{filename}' was not found and it is not allowed to create it "
                                    f"(auto_create=False)")

        self.__default_data__ = default_data
        self.__filename__ = filename
        self.__auto_save__ = auto_save

    def save(self, filename: str = None, encoding='utf-8'):
        """
        Saves your dict-like data into JSON-file. If another filename is not specified, it will save to
        filename given on initialization

        :param str filename: (optional) file to save data to (default is None)
        :param encoding: (default is 'utf-8')

        :return: None
        """
        if not filename:
            filename = self.__filename__

        self.__data__.save_to(filename, encoding=encoding)

    def reset_to_default(self):
        """
        Reset data to data given on initialization as 'default_data'

        :return: None
        """
        self.__data__ = DictHandler(self.__default_data__)
        if self.__auto_save__:
            self.save()

    def delete_file(self):
        """
        Deletes JSON-file

        :return: None
        """
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
