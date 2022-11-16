from .simple import Preprocessor as SimplePreprocessor

DISPATCH = {
    'simple': SimplePreprocessor
}


class Factory:
    """
    Создает экземпляр препроцессора по конфигу.
    Доступные реализации:
        - simple: приводит в нижний регистр и удаляет пунктуацию
    """

    def __init__(self, config):
        self.config = config

    def create(self):
        type_ = self.config['type']
        params = self.config.get('params', {})
        type_ = DISPATCH[type_]
        ob = type_(**params)
        return ob
