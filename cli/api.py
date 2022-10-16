import os

import click
import yaml

from tinysearch.api import TinysearchAPI


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
    api = TinysearchAPI()
    api.train(config=config)


@_dispatch.command()
@click.argument('src')
def predict(src):
    config = os.path.join(src, 'config.yaml')
    config = _load_config(config)
    api = TinysearchAPI()
    api.predict(src=src, config=config)


if __name__ == '__main__':
    _dispatch()
