import logging

from .corpus.factory import Factory as CorpusFactory
from .engine.factory import Factory as EngineFactory


class API:

    def __init__(self, config):
        self.config = config
        self.logger = _create_logger(self.config)

    def load_corpus(self):
        self.logger.info('Loading corpus...')
        self.logger.info('Loading...')
        corpus_factory = CorpusFactory(self.config['corpus'])
        corpus = corpus_factory.create()
        self.logger.info(f'Corpus size: {len(corpus)}')
        self.logger.info('Done.')
        return corpus

    def load_engine(self):
        self.logger.info('Loading engine...')
        engine_factory = EngineFactory(self.config['engine'])
        self.logger.info(f'Loading...')
        engine = engine_factory.load()
        self.logger.info(f'Saving...')
        self.logger.info(f'Done.')
        return engine

    def train_engine(self):
        logger = self.logger
        config = self.config
        logger.info('Training engine...')
        logger.info(f'Loading corpus...')
        corpus_factory = CorpusFactory(config['corpus'])
        corpus = corpus_factory.create()
        logger.info(f'Corpus size: {len(corpus)}')
        engine_factory = EngineFactory(config['engine'])
        engine = engine_factory.create()
        logger.info(f'Training engine...')
        engine.train(corpus)
        logger.info(f'Saving...')
        dst = config['engine']['dst']
        engine.save(dst)
        logger.info(f'Done.')


def _create_logger(config):
    level = config.get('logs', 'INFO')
    logger = logging.getLogger('api')
    logger.setLevel(level)
    logging.basicConfig()
    return logger
