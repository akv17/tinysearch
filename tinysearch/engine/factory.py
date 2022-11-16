from .bow import Engine as BOWEngine
from .bm25 import Engine as BM25Engine
from .ctx import Engine as CtxEngine

DISPATCH = {
    'bow': BOWEngine,
    'bm25': BM25Engine,
    'ctx': CtxEngine
}


class Factory:
    """
    Создает или загружает индексированный экземпляр поискового движка по конфигу.
    Доступные реализации:
        - bow: мешок слов
        - bm25: метрика Okapi BM25
        - ctx: контекстные векторы
    """

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
