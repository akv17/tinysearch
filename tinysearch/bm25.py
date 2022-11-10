import os
import pickle

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .data import Score
from .preprocess import SimplePreprocessor


class Engine:

    @classmethod
    def build(cls):
        preprocessor = SimplePreprocessor()
        count_vectorizer = CountVectorizer()
        tfidf_vectorizer = TfidfVectorizer(use_idf=True, norm='l2')
        engine = cls(
            preprocessor=preprocessor,
            count_vectorizer=count_vectorizer,
            tfidf_vectorizer=tfidf_vectorizer
        )
        return engine

    @classmethod
    def from_trained(cls, src):
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

        # матрица tf + понадобится для индексации запроса
        count = self.count_vectorizer.fit_transform(texts).toarray()
        tf = count

        # для расчета idf
        tfidf = self.tfidf_vectorizer.fit_transform(texts).toarray()

        # расчет idf
        idf = self.tfidf_vectorizer.idf_  # формула idf в sklearn: log((N+1)/(n+1))+1, и нам это ок
        idf = np.expand_dims(idf, axis=0)  # необязательно благодаря broadcast

        # расчет количества слов в каждом документе - l(d)
        len_d = tf.sum(axis=1)

        # расчет среднего количества слов документов корпуса - avdl
        avdl = len_d.mean()

        # расчет числителя
        A = idf * tf * (self.k_const + 1)

        # расчет знаменателя
        B_1 = (self.k_const * (1 - self.b_const + self.b_const * len_d / avdl))
        B_1 = np.expand_dims(B_1, axis=-1)
        B = tf + B_1

        # BM25\n"
        matrix = A / B
        self._matrix = matrix
        self._ids = np.array(corpus.ids)

    def save(self, dst):
        os.makedirs(dst, exist_ok=True)
        fp = os.path.join(dst, 'data.pkl')
        data = {
            'preprocessor': self.preprocessor,
            'count_vectorizer': self.count_vectorizer,
            'tfidf_vectorizer': self.tfidf_vectorizer,
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
        mask = np.argsort(scores)
        mask = mask[-k:][::-1]
        scores = scores[mask]
        scores = scores.tolist()
        ids = self._ids[mask].tolist()
        scores = [Score(id=i, score=s) for i, s in zip(ids, scores)]
        return scores
