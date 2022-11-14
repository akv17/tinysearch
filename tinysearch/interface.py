"""
Абстрактные интерфейсы основных компонентов приложения
"""

from abc import ABC, abstractmethod
from typing import List

from .data import Corpus, Score


class ICorpusBuilder(ABC):
    """
    Загружает корпус документов для индексации
    """

    @abstractmethod
    def create(self) -> Corpus:
        """
        Загружает корпус документов для индексации
        :return:
        """


class IPreprocessor(ABC):
    """
    Выполняет препроцессинг строк
    """

    @abstractmethod
    def run(self, text: str) -> str:
        """
        Выполняет препроцессинг входной строки
        :param text:
        :return:
        """


class IEngine:
    """
    Выполняет все функции, связанные с поисковым движком.
    В них входят:
        1. Создание с нуля по конфигу
        2. Загрузка из сохраненного на диск индекса
        3. Индексация на корпусе
        4. Поиск по индексу
        5. Сохранение индекса на диск
    """

    @classmethod
    @abstractmethod
    def create(cls, config: dict) -> 'IEngine':
        """
        Создает с нуля новый экземпляр движка по конфигу
        :param config: конфиг
        :return:
        """

    @classmethod
    @abstractmethod
    def load(cls, src: str) -> 'IEngine':
        """
        Загружает экземпляр движка из сохраненного на диск индекса
        :param src: папка с сохраненным индексом
        :return:
        """

    @abstractmethod
    def index(self, corpus: Corpus) -> None:
        """
        Индексирует движок на корпусе
        :param corpus: корпус
        :return:
        """

    @abstractmethod
    def search(self, text: str, k: int = 1) -> List[Score]:
        """
        Выполняет поиск по индексу
        :param text: запросу
        :param k: количество возвращаемых результатов
        :return:
        """

    @abstractmethod
    def save(self, dst: str) -> None:
        """
        Сохраняет индекс на диск для дальнейшего переиспользования
        :param dst: папка для сохранения индекса
        :return:
        """
