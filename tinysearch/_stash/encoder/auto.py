from .document_term import DocumentTermEncoderFactory


class AutoEncoder:
    _DISPATCH = {
        'document_term': DocumentTermEncoderFactory
    }

    @classmethod
    def create(cls, config, preprocessor):
        type_ = config['type']
        params = config['params']
        factory = cls._DISPATCH[type_]
        ob = factory(preprocessor=preprocessor, **params).create()
        return ob
