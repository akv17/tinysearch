from .data import Corpus
from .tfidf import Engine as TfidfEngine

_ENGINE_DISPATCH = {
    'tfidf': TfidfEngine
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
            scores = engine.search(query, k=2)
            for i, score in enumerate(scores):
                doc = corpus[score.id]
                text = doc.text
                text_too_long = len(text) > 30
                text = text[:30]
                text = text + '...' if text_too_long else text
                print(f'\t{i+1}. {repr(text)} [{score.score:.4f}]')
