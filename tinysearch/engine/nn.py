import os

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

from .common.rank import rank_ids_by_scores


class Engine:

    @classmethod
    def create(cls, config):
        checkpoint = config['checkpoint']
        encoder = Encoder.load(checkpoint)
        engine = cls(encoder)
        return engine

    @classmethod
    def load(cls, src):
        fp = os.path.join(src, 'checkpoint.txt')
        with open(fp, 'r') as f:
            checkpoint = f.read().strip()
        encoder = Encoder.load(checkpoint)
        engine = cls(encoder=encoder)
        fp = os.path.join(src, 'data.npz')
        data = np.load(fp)
        engine._vectors = data['vectors']
        engine._ids = data['ids']
        return engine

    def __init__(self, encoder):
        self.encoder = encoder

        self._vectors = None
        self._ids = None

    def train(self, corpus):
        vectors = np.array([self.encoder.encode(d.text) for d in corpus])
        self._vectors = vectors
        self._ids = np.array(corpus.ids)

    def search(self, text, k=1):
        vector = self.encoder.encode(text)
        vector = vector.reshape(1, -1)
        scores = cosine_similarity(self._vectors, vector)
        scores = scores.ravel()
        scores = rank_ids_by_scores(ids=self._ids, scores=scores, k=k)
        return scores

    def save(self, dst):
        os.makedirs(dst, exist_ok=True)
        fp = os.path.join(dst, 'data.npz')
        np.savez(fp, vectors=self._vectors, ids=self._ids)
        fp = os.path.join(dst, 'checkpoint.txt')
        with open(fp, 'w') as f:
            f.write(self.encoder.checkpoint)


class Encoder:

    @classmethod
    def load(cls, checkpoint):
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModel.from_pretrained(checkpoint)
        model.eval()
        ob = cls(checkpoint=checkpoint, tokenizer=tokenizer, model=model)
        return ob

    def __init__(self, checkpoint, tokenizer, model):
        self.checkpoint = checkpoint
        self.tokenizer = tokenizer
        self.model = model

    def encode(self, text):
        with torch.no_grad():
            encoded_input = self.tokenizer([text], padding=True, truncation=True, return_tensors='pt')
            model_output = self.model(**encoded_input)
            sentence_embeddings = self._pool(model_output, encoded_input['attention_mask'])
            sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
            vector = sentence_embeddings.numpy()[0]
        return vector

    def _pool(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
