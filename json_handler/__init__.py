from pathlib import Path
import os

from json_handler.utils import save_as_json, load_from_json, create_new_file


class List(list):
    def __init__(self, seq=(), on_change=None):
        if on_change is None:
            self.__on_change__ = lambda x: None
        else:
            self.__on_change__ = on_change
        super().__init__(seq)

    def clear(self) -> None:
        super().clear()
        self.__on_change__('list.clear')

    def pop(self, __index=...):
        res = super().pop(__index)
        self.__on_change__('list.pop')
        return res

    def append(self, __object) -> None:
        super().append(__object)
        self.__on_change__('list.append')

    def extend(self, __iterable) -> None:
        super().extend(__iterable)
        self.__on_change__('list.extend')

    def remove(self, __value) -> None:
        super().remove(__value)
        self.__on_change__('list.remove')

    def insert(self, __index, __object) -> None:
        super().insert(__index, __object)
        self.__on_change__('list.insert')

    def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
        super().sort(key=..., reverse=...)
        self.__on_change__('list.sort')

    def reverse(self) -> None:
        super().reverse()
        self.__on_change__('list.reverse')


class DictHandler(dict):
    def __init__(self, d=None, on_change=None, **kwargs):
        self.__data__ = {}
        if on_change is None:
            self.__on_change__ = lambda x: None
        else:
            self.__on_change__ = on_change
        if d:
            self.update(**d)
        if kwargs:
            self.update(**kwargs)

    def update(self, __m=None, **kwargs) -> None:
        if __m is None:
            __m = {}
        for key, value in __m.items():
            self.__setattr__(key, value)
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        self.__on_change__(f'dict.update')

    def clear(self) -> None:
        self.__data__.clear()
        self.__on_change__('dict.clear')

    def copy(self):
        return self.__data__.copy()

    @classmethod
    def fromkeys(cls, __iterable, __value: None = ...) -> dict:
        return dict.fromkeys(__iterable, __value)

    def get(self, key):
        return self.__data__.get(key)

    def items(self):
        return self.__data__.items()

    def keys(self):
        return self.__data__.keys()

    def pop(self, key):
        res = self.__data__.pop(key)
        self.__on_change__('dict.pop')
        return res

    def popitem(self):
        res = self.__data__.popitem()
        self.__on_change__('dict.popitem')
        return res

    def setdefault(self, __key, __default=...):
        return self.__data__.setdefault(__key, __default)

    def values(self):
        return self.__data__.values()

    def set(self, k, v):
        self.__dict__[k] = v

    def __getattr__(self, item):
        return self.__data__[item]

    __getitem__ = __getattr__

    def __setattr__(self, key, value):
        if key in ('__on_change__', '__data__'):
            self.set(key, value)
            return
        if isinstance(value, tuple):
            value = [DictHandler(x, self.__on_change__)
                     if isinstance(x, dict) else x for x in value]
            value = tuple(value)
        elif isinstance(value, list):
            value = List([DictHandler(x, self.__on_change__)
                          if isinstance(x, dict) else x for x in value], self.__on_change__)
        elif isinstance(value, dict) and not isinstance(value, DictHandler):
            value = DictHandler(value, self.__on_change__)

        self.__data__[key] = value
        self.__on_change__('dict.setattr')

    __setitem__ = __setattr__

    def __delitem__(self, key):
        del self.__data__[key]
        self.__on_change__('dict.del')

    __delattr__ = __delitem__

    def __str__(self):
        return str(self.__data__)

    def __repr__(self):
        return self.__data__.__repr__()

    def __cmp__(self, dict_):
        return self.__cmp__(self.__data__, dict_)

    def __contains__(self, item):
        return item in self.__data__

    def __iter__(self):  # for dict()
        return iter(self.__data__)

    def __len__(self):  # for pprint()
        return len(self.__data__)


class JsonHandler(DictHandler):
    """
    Class helps you handling JSON-like files as if it was an objects with attributes
    """

    def __init__(self, filename: str = None, data: dict = None, default_data: dict = None, auto_save=False,
                 encoding: str = 'utf-8'):
        """
        :param str filename: name of JSON-like file to handle
        :param dict data: data you can pass on initialization (default is None)
        :param dict default_data: data which will be applied if there is no data in JSON-file
        and 'data' parameter not provided (default is None)
        :param bool auto_save: if True it will save data to JSON-file each time data is changing (default is True)
        :param bool auto_create: if True file will automatically creates if it does not exist
        :param str encoding: encoding to work with JSON files

        :raises AssertionError: if there is no such filename and 'auto_save' = True
        """
        super().__init__()
        if not data:
            data = {}
        if not default_data:
            default_data = {}
        self.set('__default_data__', default_data)
        self.set('__filename__', filename)
        self.set('__auto_save__', auto_save)
        self.set('__encoding__', encoding)

        self.__on_change__ = lambda x: self._auto_save(x)

        assert not (not filename and auto_save), "Filename should be provided to use 'auto_save'"

        data = data if data else default_data

        if filename and Path(filename).exists():
            # print('Loading from file...')
            file_data = load_from_json(filename, encoding=encoding)
            self.update(file_data)

        self.update(data)

    def _auto_save(self, action: str = None):
        if self.__auto_save__:
            self.save(_action=action)

    def save(self, filename: str = None, encoding=None, _action: str = None):
        """
        Saves your dict-like data into JSON-file. If another filename is not specified, it will save to
        filename given on initialization

        :param str filename: (optional) file to save data to (default is None)
        :param encoding: (default is 'utf-8')

        :return: None
        """
        # print(f'Changes ({_action}). Saving...', self)
        if not encoding:
            encoding = self.__encoding__
        if not filename:
            filename = self.__filename__

        assert filename, "No filename was provided!"

        save_as_json(filename, self.__data__, encoding=encoding)

    def reset_to_default(self):
        """
        Reset data to data given on initialization as 'default_data'

        :return: None
        """
        self.clear()
        self.update(**self.__default_data__)

    def delete_file(self):
        """
        Deletes JSON-file

        :return: None
        """
        os.remove(self.__filename__)

