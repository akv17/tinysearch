from .corpus.auto import AutoCorpus
from .preprocessor.auto import AutoPreprocessor
from .encoder.auto import AutoEncoder


class TinysearchAPI:

    def train(self, config):
        cmd = TrainCommand(config=config)
        cmd.run()

    def predict(self, config):
        pass


class TrainCommand:

    def __init__(self, config):
        self.config = config

    def run(self):
        corpus = AutoCorpus.create(self.config['corpus'])
        preprocessor = AutoPreprocessor.create(self.config['preprocessor'])
        encoder = AutoEncoder.create(self.config['encoder'])
        encoder.set_preprocessor(preprocessor)
        return
