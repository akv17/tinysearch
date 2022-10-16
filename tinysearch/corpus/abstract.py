from abc import ABC, abstractmethod


class ICorpus(ABC):

    @abstractmethod
    def __len__(self): pass

    @abstractmethod
    def __iter__(self): pass

    @abstractmethod
    def __getitem__(self, item): pass


class ICorpusBuilder(ABC):

    @abstractmethod
    def create(self): pass
