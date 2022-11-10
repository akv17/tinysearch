import os
import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .data import Score
from .preprocess import SimplePreprocessor


class Engine:

    @classmethod
    def build(cls):
        vectorizer = TfidfVectorizer()
        preprocessor = SimplePreprocessor()
        engine = cls(vectorizer=vectorizer, preprocessor=preprocessor)
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

    def __init__(self, vectorizer, preprocessor):
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor

        self._matrix = None
        self._ids = None

    def train(self, corpus):
        texts = [self.preprocessor.run(d.text) for d in corpus]
        self.vectorizer.fit(texts)
        self._matrix = self.vectorizer.transform(texts)
        self._ids = np.array(corpus.ids)

    def save(self, dst):
        os.makedirs(dst, exist_ok=True)
        fp = os.path.join(dst, 'data.pkl')
        data = {
            'vectorizer': self.vectorizer,
            'preprocessor': self.preprocessor,
            'matrix': self._matrix,
            'ids': self._ids,
        }
        with open(fp, 'wb') as f:
            pickle.dump(data, f)

    def search(self, text, k=1):
        text = self.preprocessor.run(text)
        vector = self.vectorizer.transform([text])
        scores = cosine_similarity(self._matrix, vector)
        scores = scores.ravel()
        mask = np.argsort(scores)
        mask = mask[-k:][::-1]
        scores = scores[mask]
        scores = scores.tolist()
        ids = self._ids[mask].tolist()
        scores = [Score(id=i, score=s) for i, s in zip(ids, scores)]
        return scores
