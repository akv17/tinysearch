from abc import ABC, abstractmethod
from typing import List

from .data import Corpus, Score


class ICorpusBuilder(ABC):

    @abstractmethod
    def create(self) -> Corpus:
        pass


class IPreprocessor(ABC):

    @abstractmethod
    def run(self, text: str) -> str:
        pass


class IEngine:

    @classmethod
    @abstractmethod
    def create(cls, config: dict) -> 'IEngine':
        pass

    @classmethod
    @abstractmethod
    def load(cls, src: str) -> 'IEngine':
        pass

    @abstractmethod
    def train(self, corpus: Corpus) -> None:
        pass

    @abstractmethod
    def search(self, text: str, k: int = 1) -> List[Score]:
        pass

    @abstractmethod
    def save(self, dst: str) -> None:
        pass
