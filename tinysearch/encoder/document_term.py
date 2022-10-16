from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class DocumentTermEncoder:

    def __init__(self, vectorizer, preprocessor=None):
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor

    def set_preprocessor(self, ob):
        self.preprocessor = ob

    def train(self, documents):
        pass

    def encode_batch(self, documents):
        pass

    def encode(self, document):
        pass


class DocumentTermEncoderFactory:
    _VECTORIZER_DISPATCH = {
        'count': CountVectorizer,
        'tfidf': TfidfVectorizer
    }

    def __init__(self, vectorizer, preprocessor=None):
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor

    def create(self):
        vectorizer = self._VECTORIZER_DISPATCH[self.vectorizer]
        ob = DocumentTermEncoder(vectorizer=vectorizer)
        return ob
