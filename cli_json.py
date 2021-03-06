from __future__ import annotations

import sys
import functools
from logging import getLogger

import click

from modules.create_json import CreateJson

logger = getLogger(__name__)


def common_options(func):
    @ click.option('-i', '--input_dir', required=True, type=str,
                   default='./data',
                   help="glob target file dir.(default: ./data)")
    @ click.option('-o', '--output_dir', required=True, type=str,
                   default='./data',
                   help="output dir.(default: ./data)")
    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@ click.command()
@ common_options
def cli(input_dir, output_dir):
    response_code: int = 1
    app = CreateJson(input_dir)
    response_code = app.json_dumper(output_dir)
    if response_code != 0:
        print(f"Error code: {response_code}")
        sys.exit(1)
    sys.exit(0)


def main():
    cli()


if __name__ == "__main__":
    main()
