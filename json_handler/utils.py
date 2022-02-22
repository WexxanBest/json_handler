import json


def load_from_json(filename: str, encoding: str = 'utf-8') -> dict:
    with open(filename, mode='r', encoding=encoding) as file:
        _data = file.read()
        if not len(_data):
            data = {}
        else:
            data = json.loads(_data)
    return data


def save_as_json(filename: str, data: dict, encoding: str = 'utf-8') -> None:
    with open(filename, mode='w', encoding=encoding) as file:
        json.dump(data, file)


def create_new_file(filename: str) -> None:
    open(filename, 'w').close()
