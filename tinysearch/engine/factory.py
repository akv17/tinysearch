from .vectorized import Engine as VectorizedEngine
from .bm25 import Engine as BM25Engine
from .nn import Engine as NNEngine

DISPATCH = {
    'vectorized': VectorizedEngine,
    'bm25': BM25Engine,
    'nn': NNEngine
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
