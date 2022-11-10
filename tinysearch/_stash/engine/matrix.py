import numpy as np

from tinysearch.data import Score


class MatrixEngine:

    def __init__(self, index):
        self.index = index

    def predict(self, document, k=5):
        encoding = self.index.encode(document)
        scores = encoding.matrix.dot(encoding.vector.T)
        scores = scores.toarray().ravel()
        mask = np.argsort(scores)[::-1][:k]
        scores = scores[mask]
        keys = encoding.keys[mask]
        texts = encoding.texts[mask]
        scores = [Score(key=k, score=float(s), text=t) for k, s, t in zip(keys, scores, texts)]
        return scores


class MatrixEngineFactory:

    def __init__(self, index):
        self.index = index

    def create(self):
        ob = MatrixEngine(index=self.index)
        return ob
