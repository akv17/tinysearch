import os

from .utils.logs import create_logger
from .corpus.auto import AutoCorpus
from .preprocessor.auto import AutoPreprocessor
from .index.auto import AutoIndex


class TinysearchAPI:

    def __init__(self, logger=None):
        self.logger = logger or create_logger('tinysearch')

    def train(self, config):
        cmd = TrainCommand(config=config, logger=self.logger)
        cmd.run()

    def predict(self, config):
        pass


class TrainCommand:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self):
        self.logger.info('-> Start training...')
        self.logger.info(f'-> Loading corpus...')
        corpus = AutoCorpus.create(self.config['corpus'])
        preprocessor = AutoPreprocessor.create(self.config['preprocessor'])
        index = AutoIndex.create(config=self.config['index'], preprocessor=preprocessor)
        self.logger.info(f'-> Training index...')
        index.train(corpus)
        dst = self.config['dst']
        os.makedirs(dst, exist_ok=True)
        self.logger.info(f'-> Saving index: {dst}')
        index.save(dst)
        self.logger.info('-> Done.')
