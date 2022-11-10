import os

import click
import yaml

from tinysearch.api import API


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
    api = API()
    api.train(config)


@_dispatch.command()
@click.argument('config')
def search(config):
    config = _load_config(config)
    api = API()
    api.predict(config)


if __name__ == '__main__':
    _dispatch()
