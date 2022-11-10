from .single_file import Factory as SingleFileFactory

DISPATCH = {
    'single_file': SingleFileFactory
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
