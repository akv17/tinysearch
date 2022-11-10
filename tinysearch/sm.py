import os

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

from .data import Score


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class Engine:

    @classmethod
    def build(cls):
        checkpoint = 'sentence-transformers/all-MiniLM-L6-v2'
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModel.from_pretrained(checkpoint)
        model.eval()
        engine = cls(tokenizer=tokenizer, model=model)
        return engine

    @classmethod
    def from_trained(cls, src):
        checkpoint = 'sentence-transformers/all-MiniLM-L6-v2'
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModel.from_pretrained(checkpoint)
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
            encoded_input = self.tokenizer([text], padding=True, truncation=True, return_tensors='pt')
            model_output = self.model(**encoded_input)
            sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
            sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
            vector = sentence_embeddings.numpy()[0]
        return vector
