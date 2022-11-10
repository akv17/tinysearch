from .simple import Preprocessor as SimplePreprocessor

_DISPATCH = {
    'simple': SimplePreprocessor
}


def create_preprocessor(config):
    type_ = config['type']
    params = config.get('params', {})
    type_ = _DISPATCH[type_]
    ob = type_(**params)
    return ob
