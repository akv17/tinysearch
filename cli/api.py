import click
from yaml import safe_load as yaml_safe_load

from tinysearch.api import TinysearchAPI


def _load_config(fp):
    with open(fp, 'r') as f:
        config = yaml_safe_load(f)
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


if __name__ == '__main__':
    _dispatch()
