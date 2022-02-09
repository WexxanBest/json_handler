import json
from pathlib import Path
import os


def load_from_json(filename: str, encoding: str = 'utf-8'):
    with open(filename, mode='r', encoding=encoding) as file:
        _data = file.read()
        if not len(_data):
            data = {}
        else:
            data = json.loads(_data)
    return data


def save_to_json(filename: str, data: dict, encoding: str = 'utf-8'):
    with open(filename, mode='w', encoding=encoding) as file:
        json.dump(data, file)


class DictHandler(dict):
    """
    Class helps you to handle Python dict as if it was an objects with attributes
    """

    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        if kwargs:
            d.update(**kwargs)
        for k, v in d.items():
            setattr(self, k, v)

    def update(self, e=None, **f):
        d = e or dict()
        d.update(f)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):
        return super().pop(k, d)

    def set(self, key, value):
        self.__dict__[key] = value

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = [DictHandler(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, dict) and not isinstance(value, DictHandler):
            value = DictHandler(value)
        super().__setattr__(name, value)
        super().__setitem__(name, value)

    __setitem__ = __setattr__

    def __delattr__(self, item):
        del self[item]


class JsonHandler(DictHandler):
    """
    Class helps you handling JSON-like files as if it was an objects with attributes
    """

    def __init__(self, filename: str, data: dict = None, default_data: dict = None, auto_save=False, auto_create=False,
                 encoding: str = 'utf-8'):
        """
        :param str filename: name of JSON-like file to handle
        :param dict data: data you can pass on initialization (default is None)
        :param dict default_data: data which will be applied if there is no data in JSON-file
        and 'data' parameter not provided (default is None)
        :param bool auto_save: if True it will save data to JSON-file each time data is changing (default is True)
        :param bool auto_create: if True file will automatically creates if it does not exist
        :param str encoding: encoding to work with JSON files

        :raises FileNotFoundError: if there is no such filename and 'auto_create' = False
        """
        if not data:
            data = {}
        if not default_data:
            default_data = {}
        self.set('__default_data__', default_data)
        self.set('__filename__', filename)
        self.set('__auto_save__', auto_save)
        self.set('__encoding__', encoding)
        if not Path(filename).exists() and auto_create:  # create file if it doesn't exist and 'auto_create' = True
            if data:
                super().__init__(data)
            else:
                super().__init__(default_data)

            if auto_save:
                self.save()

        elif Path(filename).exists():  # retrieve data from json file
            _data = load_from_json(filename, encoding=encoding)
            super().__init__(_data)
            self.update(data)
        else:
            raise FileNotFoundError(f"File '{filename}' was not found and it is not allowed to create it "
                                    f"(auto_create=False)")

    def save(self, filename: str = None, encoding=None):
        """
        Saves your dict-like data into JSON-file. If another filename is not specified, it will save to
        filename given on initialization

        :param str filename: (optional) file to save data to (default is None)
        :param encoding: (default is 'utf-8')

        :return: None
        """
        if not encoding:
            encoding = self.__encoding__
        if not filename:
            filename = self.__filename__

        save_to_json(filename, self, encoding=encoding)

    def reset_to_default(self):
        """
        Reset data to data given on initialization as 'default_data'

        :return: None
        """
        self.update(**self.__default_data__)
        if self.__auto_save__:
            self.save()

    def delete_file(self):
        """
        Deletes JSON-file

        :return: None
        """
        os.remove(self.__filename__)

    def update(self, e=None, **f) -> None:
        super().update(e, **f)
        if self.__auto_save__:
            self.save()

    def clear(self) -> None:
        super().clear()
        if self.__auto_save__:
            self.save()

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if self.__auto_save__:
            self.save()

    __setitem__ = __setattr__

    def __delattr__(self, item) -> None:
        super().__delattr__(item)
        if self.__auto_save__:
            self.save()

    def __delitem__(self, key) -> None:
        super().__delitem__(key)
        if self.__auto_save__:
            self.save()

