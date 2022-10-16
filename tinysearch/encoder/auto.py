from .document_term import DocumentTermEncoderFactory


class AutoEncoder:
    _DISPATCH = {
        'document_term': DocumentTermEncoderFactory
    }

    @classmethod
    def create(cls, config):
        type_ = config['type']
        params = config['params']
        factory = cls._DISPATCH[type_]
        ob = factory(**params).create()
        return ob
