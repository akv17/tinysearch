from tinysearch.data import Document, Corpus


class Factory:

    def __init__(self, path):
        self.path = path

    def create(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
        docs = [Document(id=str(i), text=ln.strip(), path=self.path) for i, ln in enumerate(lines) if ln.strip()]
        docs = sorted(docs, key=lambda _d: _d.id)
        corpus = Corpus(docs)
        return corpus
