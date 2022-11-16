from .single_file import Builder as SingleFileBuilder
from .multi_file import Builder as MultiFileBuilder

DISPATCH = {
    'single_file': SingleFileBuilder,
    'multi_file': MultiFileBuilder,
}


class Factory:
    """
    Загружает экземпляр корпуса по конфигу.
    Делегирует логику загрузчику под каждый доступный формат:
        - single_file: весь корпус в одном файле, а одним документом считается одна строка
        - multi_file: читает все файлы внутри папки, а одним документом считается один файл
    """

    def __init__(self, config):
        self.config = config

    def create(self):
        type_ = self.config['type']
        params = self.config['params']
        factory = DISPATCH[type_]
        factory = factory(**params)
        corpus = factory.create()
        return corpus
