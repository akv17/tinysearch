from .file import FileCorpusFactory


class AutoCorpus:
    _DISPATCH = {
        'file': FileCorpusFactory
    }

    @classmethod
    def create(cls, config):
        type_ = config['type']
        params = config['params']
        factory = cls._DISPATCH[type_]
        ob = factory(**params).create()
        return ob
