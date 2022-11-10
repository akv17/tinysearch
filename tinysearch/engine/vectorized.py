import os
import pickle

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .utils.rank import rank_ids_by_scores
from ..preprocessor.factory import create_preprocessor


VECTORIZER_DISPATCH = {
    'tfidf': TfidfVectorizer,
    'count': CountVectorizer
}


class Engine:

    @classmethod
    def create(cls, config):
        preprocessor = create_preprocessor(config['preprocessor'])
        vectorizer_type = config['vectorizer']['type']
        vectorizer_type = VECTORIZER_DISPATCH[vectorizer_type]
        vectorizer_params = config['vectorizer'].get('params', {})
        vectorizer = vectorizer_type(**vectorizer_params)
        engine = cls(vectorizer=vectorizer, preprocessor=preprocessor)
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

    def __init__(self, preprocessor, vectorizer):
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer

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
        scores = rank_ids_by_scores(ids=self._ids, scores=scores, k=k)
        return scores
