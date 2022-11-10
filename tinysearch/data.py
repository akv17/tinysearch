from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    id: str
    text: str


@dataclass
class Score:
    id: str
    score: float


class Corpus:

    @classmethod
    def load(cls, fp):
        with open(fp, 'r') as f:
            lines = f.readlines()
        docs = [Document(id=str(i), text=ln.strip()) for i, ln in enumerate(lines) if ln.strip()]
        corpus = cls(docs)
        return corpus

    def __init__(self, documents):
        self.documents = documents

    def __len__(self):
        return len(self.documents)

    def __iter__(self):
        return iter(self.documents)

    def __getitem__(self, item):
        return self.documents[item]
