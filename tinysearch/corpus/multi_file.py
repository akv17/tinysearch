import os

from tinysearch.data import Document, Corpus

from ..interface import ICorpusBuilder


class Builder(ICorpusBuilder):
    """
    Загружает корпус, рекурсивно обходя всю папку, где один файл считается одним документом
    """

    def __init__(self, path):
        self.path = path

    def create(self):
        """
        Загружает корпус
        :return:
        """
        id_ = 0
        docs = []
        for cur_root, _, cur_files in os.walk(self.path):
            for fn in cur_files:
                fp = os.path.join(cur_root, fn)
                with open(fp, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                doc = Document(id=str(id_), text=text, path=fp)
                docs.append(doc)
                id_ += 1
        docs = sorted(docs, key=lambda _d: _d.id)
        corpus = Corpus(docs)
        return corpus
