import yaml

from tinysearch.api import API

_API = None
_FILE_NAME = None


def get_or_load_api(file):
    global _API
    global _FILE_NAME
    if file is None:
        return _API
    if file.name == _FILE_NAME:
        return _API
    config = yaml.safe_load(file)
    api = API(config)
    api.load()
    _API = api
    _FILE_NAME = file.name
    return _API
