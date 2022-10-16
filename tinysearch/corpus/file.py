import os

from .abstract import ICorpus, ICorpusBuilder
from ..data import Document


class FileCorpus(ICorpus):

    def __init__(self, documents):
        self.documents = documents

    def __len__(self):
        return len(self.documents)

    def __iter__(self):
        return iter(self.documents)

    def __getitem__(self, item):
        return self.documents[item]


class FileCorpusBuilder:

    def __init__(self, root):
        self.root = root

    def create(self):
        docs = []
        for fn in os.listdir(self.root):
            fp = os.path.join(self.root, fn)
            key, _ = os.path.splitext(fn)
            with open(fp, 'r', encoding='utf-8') as f:
                text = f.read()
            doc = Document(key=key, text=text)
            docs.append(doc)
        corpus = FileCorpus(documents=docs)
        return corpus
