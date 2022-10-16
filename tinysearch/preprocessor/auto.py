from .impl import (
    IdentityPreprocessor,
    AlphanumericPreprocessor
)


class AutoPreprocessor:
    _DISPATCH = {
        'identity': IdentityPreprocessor,
        'alphanum': AlphanumericPreprocessor
    }

    @classmethod
    def create(cls, config):
        type_ = config['type']
        params = config['params']
        cls_ = cls._DISPATCH[type_]
        ob = cls_(**params)
        return ob
