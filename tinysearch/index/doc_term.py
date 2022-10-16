import os
import pickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class DocumentTermIndex:

    def __init__(self, vectorizer, preprocessor):
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor

        self._data = None
        self._keys = None
        self._token_keys = None

    def train(self, documents):
        keys = [d.key for d in documents]
        texts = [d.text for d in documents]
        texts = [self.preprocessor.run(t) for t in texts]
        self._data = self.vectorizer.fit_transform(texts)
        self._keys = keys
        self._token_keys = self.vectorizer.get_feature_names_out()

    def encode(self, document):
        text = document.text
        text = self.preprocessor(text)
        data = self.vectorizer.transform([text])
        return data

    def encode_batch(self, documents):
        texts = [d.text for d in documents]
        texts = [self.preprocessor.run(t) for t in texts]
        data = self.vectorizer.transform(texts)
        return data

    def save(self, dst):
        fp = os.path.join(dst, 'index.pkl')
        data = {
            'data': self._data,
            'keys': self._keys,
            'token_keys': self._token_keys
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
        pass
