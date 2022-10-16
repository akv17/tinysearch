from .doc_term import DocumentTermIndexFactory


class AutoIndex:
    _DISPATCH = {
        'doc_term': DocumentTermIndexFactory
    }

    @classmethod
    def create(cls, config, preprocessor):
        type_ = config['type']
        params = config.get('params', {})
        factory = cls._DISPATCH[type_]
        ob = factory(preprocessor=preprocessor, **params).create()
        return ob
