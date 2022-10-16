import os

import yaml

from .utils.logs import create_logger
from .data import Document
from .corpus.auto import AutoCorpus
from .preprocessor.auto import AutoPreprocessor
from .index.auto import AutoIndex
from .engine.auto import AutoEngine


class TinysearchAPI:

    def __init__(self, logger=None):
        self.logger = logger or create_logger('tinysearch')

    def train(self, config):
        cmd = TrainCommand(config=config, logger=self.logger)
        cmd.run()

    def predict(self, src, config):
        cmd = PredictCommand(src=src, config=config, logger=self.logger)
        cmd.run()


class TrainCommand:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self):
        self.logger.info('-> Training...')
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
        self.logger.info(f'-> Saving config: {dst}')
        config_fp = os.path.join(dst, 'config.yaml')
        config_to_save = self.config.copy()
        config_to_save.pop('corpus')
        config_to_save.pop('dst')
        with open(config_fp, 'w') as f:
            yaml.safe_dump(config_to_save, f)
        index.save(dst)
        self.logger.info('-> Done.')


class PredictCommand:

    def __init__(self, src, config, logger):
        self.src = src
        self.config = config
        self.logger = logger

    def run(self):
        self.logger.info('-> Predicting...')
        preprocessor = AutoPreprocessor.create(self.config['preprocessor'])
        index = AutoIndex.load(src=self.src, config=self.config['index'], preprocessor=preprocessor)
        engine = AutoEngine.create(config=self.config['engine'], index=index)
        self._loop(engine)

    def _loop(self, engine):
        stop = False
        while not stop:
            query = input(f'---> Enter query: ').strip()
            query = Document(key=None, text=query)
            result = engine.predict(query)
            for score in result:
                print(f'\t-> {score}')
            print()
