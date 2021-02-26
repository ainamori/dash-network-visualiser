import functools
import pathlib
import sys
from logging import getLogger
# from nested_lookup import nested_lookup
import json
from __future__ import annotations

import click

logger = getLogger(__name__)


class Runner:

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir: str = input_dir
        self.output_dir: str = output_dir
        self.node_json: str = "node.json"
        self.edge_json: str = "edge.json"

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
        except OSError as e:
            msg = "Cannot load file: %s" % str(e)
            logger.error(msg, exc_info=True)
            raise Exception
        return path_obj_list

    def _find_node(self, node, node_list):
        


    def _generate_net_json(self, path_obj_list):
        node_json_path = "/".join([self.output_dir, self.node_json])
        edge_json_path = "/".join([self.output_dir, self.edge_json])

        for path_obj in path_obj_list:
            try:
                with open(path_obj) as f:
                    load_data = json.load(f)
                for source_port, target_info in load_data.items():



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


            except OSError as e:
                logger.error(str(e))





            for _node in list(set(node_list)):
                __node = {
                    "name": _node,
                    "icon": "./images/switch.png",
                }
                inet_henge["nodes"].append(__node)
            write_path.write_text(json.dumps(inet_henge, indent=2))
            msg = None
            self.write_path.write_text(json.dumps(data, indent=2))
        except Exception as e:
            msg = str(e)
            logger.error(msg, exc_info=True)

    def run(self):
        data = []
        try:
            print("Loading lldp files.")
            path_obj_list = self._glob_dir()

            print("Generating json files.")
            self._generate_net_json(path_obj_list)
        except Exception as e:
            logger.error(str(e))
            sys.exit(1)


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
    app = Runner(input_dir, output_dir)
    app.run()


def main():
    cli()


if __name__ == "__main__":
    main()
