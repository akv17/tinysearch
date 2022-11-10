import os

import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

from .data import Score


class Engine:

    @classmethod
    def build(cls):
        checkpoint = 'bert-base-uncased'
        tokenizer = BertTokenizer.from_pretrained(checkpoint)
        model = BertModel.from_pretrained(checkpoint)
        model.eval()
        engine = cls(tokenizer=tokenizer, model=model)
        return engine

    @classmethod
    def from_trained(cls, src):
        checkpoint = 'bert-base-uncased'
        tokenizer = BertTokenizer.from_pretrained(checkpoint)
        model = BertModel.from_pretrained(checkpoint)
        model.eval()
        engine = cls(tokenizer=tokenizer, model=model)
        fp = os.path.join(src, 'data.npz')
        data = np.load(fp)
        engine._vectors = data['vectors']
        engine._ids = data['ids']
        return engine

    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

        self._vectors = None
        self._ids = None

    def train(self, corpus):
        vectors = np.array([self._vectorize(d.text) for d in corpus])
        self._vectors = vectors
        self._ids = np.array(corpus.ids)

    def search(self, text, k=1):
        vector = self._vectorize(text)
        vector = vector.reshape(1, -1)
        scores = cosine_similarity(self._vectors, vector)
        scores = scores.ravel()
        mask = np.argsort(scores)
        mask = mask[-k:][::-1]
        scores = scores[mask]
        scores = scores.tolist()
        ids = self._ids[mask].tolist()
        scores = [Score(id=i, score=s) for i, s in zip(ids, scores)]
        return scores

    def save(self, dst):
        os.makedirs(dst, exist_ok=True)
        fp = os.path.join(dst, 'data.npz')
        np.savez(fp, vectors=self._vectors, ids=self._ids)

    def _vectorize(self, text):
        with torch.no_grad():
            encoded_input = self.tokenizer(text, return_tensors='pt')
            output = self.model(**encoded_input)
            breakpoint()
            output = output.pooler_output

            vector = output.numpy()[0]
        return vector
