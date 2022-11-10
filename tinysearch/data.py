from dataclasses import dataclass


@dataclass
class Document:
    id: str
    text: str


@dataclass
class Score:
    id: str
    score: float


class Corpus:

    def __init__(self, documents):
        self.documents = documents
        self._map = {d.id: d for d in self.documents}

    @property
    def ids(self):
        return list(self._map)

    def __len__(self):
        return len(self.documents)

    def __iter__(self):
        return iter(self.documents)

    def __getitem__(self, item):
        return self._map[item]
