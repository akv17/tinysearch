import logging

from .corpus.factory import Factory as CorpusFactory
from .engine.factory import Factory as EngineFactory


class API:

    def __init__(self, config):
        self.config = config
        self.logger = _create_logger(self.config)

        self.corpus = None
        self.engine = None

    def load(self):
        self.load_corpus()
        self.load_engine()

    def load_corpus(self):
        self.logger.info('Loading corpus...')
        corpus_factory = CorpusFactory(self.config['corpus'])
        corpus = corpus_factory.create()
        self.logger.info(f'Size: {len(corpus)}')
        self.logger.info('Done.')
        self.corpus = corpus

    def load_engine(self):
        self.logger.info('Loading engine...')
        engine_factory = EngineFactory(self.config['engine'])
        self.logger.info(f'Loading...')
        engine = engine_factory.load()
        self.logger.info(f'Done.')
        self.engine = engine

    def train(self):
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
