from .file import FileCorpusBuilder


class AutoCorpus:
    _DISPATCH = {
        'file': FileCorpusBuilder
    }

    @classmethod
    def build(cls, config):
        type_ = config['type']
        params = config['params']
        builder = cls._DISPATCH[type_]
        corpus = builder(**params).create()
        return corpus
