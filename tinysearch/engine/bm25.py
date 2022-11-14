import os
import pickle

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from .common.rank import rank_ids_by_scores
from ..preprocessor.factory import Factory as PreprocessorFactory
from ..interface import IEngine


class Engine(IEngine):
    """
    Поисковый движок на базе метрики Okapi BM25.
    Выполнен в матричном виде (разрежено).
    """

    @classmethod
    def create(cls, config):
        preprocessor_config = PreprocessorFactory(config['preprocessor'])
        preprocessor = preprocessor_config.create()
        count_vectorizer = CountVectorizer()
        tfidf_vectorizer = TfidfVectorizer()
        k = config.get('const', {}).get('k', 2.0)
        b = config.get('const', {}).get('b', 0.75)
        engine = cls(
            preprocessor=preprocessor,
            count_vectorizer=count_vectorizer,
            tfidf_vectorizer=tfidf_vectorizer,
            k=k,
            b=b
        )
        return engine

    @classmethod
    def load(cls, src):
        fp = os.path.join(src, 'data.pkl')
        with open(fp, 'rb') as f:
            data = pickle.load(f)
        matrix = data.pop('matrix')
        ids = data.pop('ids')
        engine = cls(**data)
        engine._matrix = matrix
        engine._ids = ids
        return engine

    def __init__(
        self,
        preprocessor,
        count_vectorizer,
        tfidf_vectorizer,
        k=2.0,
        b=0.75
    ):
        self.preprocessor = preprocessor
        self.count_vectorizer = count_vectorizer
        self.tfidf_vectorizer = tfidf_vectorizer
        self.k_const = k
        self.b_const = b

        self._matrix = None
        self._ids = None

    def train(self, corpus):
        texts = [self.preprocessor.run(d.text) for d in corpus]
        count = self.count_vectorizer.fit_transform(texts).toarray()
        self.tfidf_vectorizer.fit(texts)
        tf = count
        idf = self.tfidf_vectorizer.idf_
        idf = np.expand_dims(idf, axis=0)
        len_d = tf.sum(axis=1)
        avdl = len_d.mean()
        a = idf * tf * (self.k_const + 1)
        b_1 = (self.k_const * (1 - self.b_const + self.b_const * len_d / avdl))
        b_1 = np.expand_dims(b_1, axis=-1)
        b = tf + b_1
        matrix = a / b
        self._matrix = matrix
        self._ids = np.array(corpus.ids)

    def save(self, dst):
        os.makedirs(dst, exist_ok=True)
        fp = os.path.join(dst, 'data.pkl')
        data = {
            'preprocessor': self.preprocessor,
            'count_vectorizer': self.count_vectorizer,
            'tfidf_vectorizer': self.tfidf_vectorizer,
            'k': self.k_const,
            'b': self.b_const,
            'matrix': self._matrix,
            'ids': self._ids,
        }
        with open(fp, 'wb') as f:
            pickle.dump(data, f)

    def search(self, text, k=1):
        text = self.preprocessor.run(text)
        vector = self.count_vectorizer.transform([text])
        scores = vector.dot(self._matrix.T)
        scores = scores.ravel()
        scores = rank_ids_by_scores(ids=self._ids, scores=scores, k=k)
        return scores
