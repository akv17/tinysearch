import click
import yaml

from tinysearch.api import API
from .mvc import Factory as SearchControllerFactory


def _load_config(fp):
    with open(fp, 'r') as f:
        config = yaml.safe_load(f)
    return config


@click.group()
def _dispatch():
    pass


@_dispatch.command()
@click.argument('config')
def train(config):
    config = _load_config(config)
    api = API(config)
    api.train_engine()


@_dispatch.command()
@click.argument('config')
def search(config):
    config = _load_config(config)
    api = API(config)
    corpus = api.load_corpus()
    engine = api.load_engine()
    controller_factory = SearchControllerFactory(corpus=corpus, engine=engine)
    controller = controller_factory.create()
    controller.run()


if __name__ == '__main__':
    _dispatch()
