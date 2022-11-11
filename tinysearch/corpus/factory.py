from .single_file import Builder as SingleFileBuilder
from .multi_file import Builder as MultiFileBuilder

DISPATCH = {
    'single_file': SingleFileBuilder,
    'multi_file': MultiFileBuilder,
}


class Factory:

    def __init__(self, config):
        self.config = config

    def create(self):
        type_ = self.config['type']
        params = self.config['params']
        factory = DISPATCH[type_]
        factory = factory(**params)
        corpus = factory.create()
        return corpus
