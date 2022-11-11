from .single_file import Factory as SingleFileFactory
from .multi_file import Factory as MultiFileFactory

DISPATCH = {
    'single_file': SingleFileFactory,
    'multi_file': MultiFileFactory,
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
