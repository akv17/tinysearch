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
    api.train()


@_dispatch.command()
@click.argument('config')
@click.option('--k', type=int, default=5)
def search(config, k=5):
    config = _load_config(config)
    api = API(config)
    api.load()
    controller_factory = SearchControllerFactory(api=api, k=k)
    controller = controller_factory.create()
    controller.run()


if __name__ == '__main__':
    _dispatch()
