import functools
import pathlib
import sys
from logging import getLogger
import json
from __future__ import annotations

import click

logger = getLogger(__name__)


class Runner:

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.write_path = pathlib.Path(f"{output_dir}/net.json")
        self.path_obj_list = self._glob_dir()

    def _glob_dir(self, regex: str = None):
        """指定ディレクトリからファイル一覧を取得する."""
        if regex is None:
            _glob_regex = "[!.]*"
        else:
            _glob_regex = regex
        try:
            _p: pathlib.Path = pathlib.Path(self.input_dir)
            obj = _p.glob(_glob_regex)
            path_obj_list = list(p for p in obj if p.is_file())
        except Exception as e:
            msg = "Cannot load file: %s" % str(e)
            logger.error(msg, exc_info=True)
            raise Exception
        return path_obj_list

    def _create_data(self, lldp_data, data):
        try:
            hostname = path_obj.stem
            node_list: List = [hostname]
            write_path = pathlib.Path(f"{self.output_dir}/{hostname}.json")
            inet_henge = {"nodes": [], "links": []}
            with open(path_obj) as f:
                lldp_data = json.load(f)
            for source_port, target_list in lldp_data.items():
                _target = target_list[0]
                node_list.append(_target["hostname"])
                _link = {
                    "source": hostname,
                    "target": _target["hostname"],
                    "meta": {
                        "interface": {
                            "source": source_port,
                            "target": _target["port"],
                        },
                    },
                }
                inet_henge["links"].append(_link)
            for _node in list(set(node_list)):
                __node = {
                    "name": _node,
                    "icon": "./images/switch.png",
                }
                inet_henge["nodes"].append(__node)
            write_path.write_text(json.dumps(inet_henge, indent=2))
            msg = None
        except Exception as e:
            msg = str(e)
            logger.error(msg, exc_info=True)
        finally:
            return msg

    def run(self):
        data = []
        for path_obj in self.path_obj_list:
            try:
                with open(path_obj) as f:
                    lldp_data = json.load(f)
                _data = self._create_data(lldp_data, data)
                data.append(_data)
            except OSError as e:
                logger.error(str(e))
            except Exception as e:
                logger.error(str(e), exc_info=True)
                sys.exit(1)
            else:
                pass
        self.write_path.write_text(json.dumps(data, indent=2))


def common_options(func):
    @click.option('-i', '--input_dir', required=True, type=str,
                  default='./',
                  help="glob target file dir.(default: ./data)")
    @click.option('-o', '--output_dir', required=True, type=str,
                  default='./',
                  help="output dir.(default: ./)")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@click.command()
@common_options
def cli(input_dir, output_dir):
    result: bool = False
    try:
        app = Runner(input_dir=input_dir, output_dir=output_dir)
        app.run()
        sys.exit(0)
    except Exception as e:
        msg: str = "Cannot run program: %s" % str(e)
        print(msg)
        sys.exit(1)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
