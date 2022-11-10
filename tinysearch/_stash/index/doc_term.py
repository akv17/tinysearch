import os
import pickle

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from tinysearch.data import MatrixEncoding


class DocumentTermIndex:

    def __init__(self, vectorizer, preprocessor):
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor

        self._data = None
        self._keys = None
        self._token_keys = None
        self._texts = None

    def train(self, documents):
        keys = [d.key for d in documents]
        texts_orig = [d.text for d in documents]
        texts = [self.preprocessor.run(t) for t in texts_orig]
        self._data = self.vectorizer.fit_transform(texts)
        self._keys = keys
        self._token_keys = self.vectorizer.get_feature_names_out()
        self._texts = texts_orig

    def encode(self, document):
        text = document.text
        text = self.preprocessor.run(text)
        vector = self.vectorizer.transform([text])
        enc = MatrixEncoding(keys=self._keys, matrix=self._data, vector=vector, texts=self._texts)
        return enc

    def save(self, dst):
        fp = os.path.join(dst, 'index.pkl')
        data = {
            'vectorizer': self.vectorizer,
            '_data': self._data,
            '_keys': np.array(self._keys),
            '_token_keys': np.array(self._token_keys),
            '_texts': np.array(self._texts)
        }
        with open(fp, 'wb') as f:
            pickle.dump(data, f)


class DocumentTermIndexFactory:
    _VECTORIZER_DISPATCH = {
        'count': CountVectorizer,
        'tfidf': TfidfVectorizer
    }

    def __init__(self, vectorizer, preprocessor):
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor

    def create(self):
        vect_type = self.vectorizer['type']
        vect_params = self.vectorizer.get('params', {})
        vectorizer = self._VECTORIZER_DISPATCH[vect_type]
        vectorizer = vectorizer(**vect_params)
        ob = DocumentTermIndex(vectorizer=vectorizer, preprocessor=self.preprocessor)
        return ob

    def load(self, src):
        fp = os.path.join(src, 'index.pkl')
        with open(fp, 'rb') as f:
            data = pickle.load(f)
        ob = DocumentTermIndex(vectorizer=None, preprocessor=self.preprocessor)
        for k, v in data.items():
            setattr(ob, k, v)
        return ob
