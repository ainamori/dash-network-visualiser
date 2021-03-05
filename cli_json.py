from __future__ import annotations

import functools
from logging import getLogger

import click

from modules.create_json import Runner

logger = getLogger(__name__)


def common_options(func):
    @ click.option('-i', '--input_dir', required=True, type=str,
                   default='./',
                   help="glob target file dir.(default: ./data)")
    @ click.option('-o', '--output_dir', required=True, type=str,
                   default='./',
                   help="output dir.(default: ./)")
    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@ click.command()
@ common_options
def cli(input_dir, output_dir):
    app = Runner(input_dir, output_dir)
    app.run()


def main():
    cli()


if __name__ == "__main__":
    main()
