from .matrix import MatrixEngineFactory


class AutoEngine:
    _DISPATCH = {
        'matrix': MatrixEngineFactory
    }

    @classmethod
    def create(cls, config, index):
        type_ = config['type']
        params = config.get('params', {})
        factory = cls._DISPATCH[type_]
        ob = factory(index=index, **params).create()
        return ob
