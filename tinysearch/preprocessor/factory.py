from .simple import Preprocessor as SimplePreprocessor

_DISPATCH = {
    'simple': SimplePreprocessor
}


class Factory:
    """
    Создает экземпляр препроцессора по конфигу.
    Доступные реализации:
        - 'simple'
    """

    def __init__(self, config):
        self.config = config

    def create(self):
        type_ = self.config['type']
        params = self.config.get('params', {})
        type_ = _DISPATCH[type_]
        ob = type_(**params)
        return ob
