"""
Основной публичный интерфейс для взаимодействия с приложением
"""

import logging

from .corpus.factory import Factory as CorpusFactory
from .engine.factory import Factory as EngineFactory


class API:
    """
    Публичный интерфейс для взаимодействия с приложением aka главная точка входа.
    Предосталвяет возможность:
        1. Загрузить корпус по конфигу
        2. Загрузить движок по конфигу
        3. Получить доступ к корпусу
        4. Получить доступ к движку
        5. Индексировать движок по конфигу и сохранить результат
    """

    def __init__(self, config):
        self.config = config
        self.logger = _create_logger(self.config)

        self.corpus = None
        self.engine = None

    def load(self):
        """
        Загрузить корпус и движок по конфигу
        :return:
        """
        self.load_corpus()
        self.load_engine()

    def load_corpus(self):
        """
        Загрузить корпус по конфигу
        :return:
        """
        self.logger.info('Loading corpus...')
        corpus_factory = CorpusFactory(self.config['corpus'])
        corpus = corpus_factory.create()
        self.logger.info(f'Size: {len(corpus)}')
        self.logger.info('Done.')
        self.corpus = corpus

    def load_engine(self):
        """
        Загрузить движок по конфигу
        :return:
        """
        self.logger.info('Loading engine...')
        engine_factory = EngineFactory(self.config['engine'])
        self.logger.info(f'Loading...')
        engine = engine_factory.load()
        self.logger.info(f'Done.')
        self.engine = engine

    def train(self):
        """
        Индексировать движок по конфигу и сохранить результат
        :return:
        """
        logger = self.logger
        config = self.config
        logger.info('Training engine...')
        self.engine.train(self.corpus)
        logger.info(f'Saving...')
        dst = config['engine']['dst']
        self.engine.save(dst)
        logger.info(f'Done.')


def _create_logger(config):
    level = config.get('logs', 'INFO')
    logger = logging.getLogger('api')
    logger.setLevel(level)
    logging.basicConfig()
    return logger
