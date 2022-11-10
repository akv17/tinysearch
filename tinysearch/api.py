from .data import Corpus
from .tfidf import Engine as TfidfEngine
from .bert import Engine as BertEngine
from .sm import Engine as SmEngine
from .bm25 import Engine as Bm25Engine

_ENGINE_DISPATCH = {
    'tfidf': TfidfEngine,
    'bert': BertEngine,
    'sm': SmEngine,
    'bm25': Bm25Engine,
}


class API:

    def train(self, config):
        dst = config['dst']
        corpus = config['corpus']
        corpus = Corpus.load(corpus)
        engine = config['engine']
        engine = _ENGINE_DISPATCH[engine]
        engine = engine.build()
        engine.train(corpus)
        engine.save(dst)

    def predict(self, config):
        src = config['dst']
        corpus = config['corpus']
        corpus = Corpus.load(corpus)
        engine = config['engine']
        engine = _ENGINE_DISPATCH[engine]
        engine = engine.from_trained(src)
        while True:
            query = input('---> ')
            query = query.strip()
            if query == 'q!':
                break
            scores = engine.search(query, k=5)
            for i, score in enumerate(scores):
                doc = corpus[score.id]
                text = doc.text
                text_too_long = len(text) > 80
                text = text[:80]
                text = text + '...' if text_too_long else text
                print(f'\t{i+1}. {repr(text)} [{score.score:.4f}]')
