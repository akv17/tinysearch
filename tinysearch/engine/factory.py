from .vectorized import Engine as VectorizedEngine

DISPATCH = {
    'vectorized': VectorizedEngine
}


class Factory:

    def __init__(self, config):
        self.config = config

    def create(self):
        type_ = self.config['type']
        engine = DISPATCH[type_]
        config = self.config['params']
        engine = engine.create(config)
        return engine

    def load(self):
        type_ = self.config['type']
        engine = DISPATCH[type_]
        dst = self.config['dst']
        engine = engine.load(dst)
        return engine
