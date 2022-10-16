from .corpus.auto import AutoCorpus


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
        corpus = AutoCorpus.build(self.config['corpus'])
        return
