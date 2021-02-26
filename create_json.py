from __future__ import annotations

import functools
import json
import pathlib
import sys
from logging import getLogger

import click
from nested_lookup import nested_lookup

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

    def _update_node_list(self, node_list, node_name, interface):
        id_list = nested_lookup('id', node_list)
        if interface is None:
            _id = node_name
            _label = node_name
            _parent = None
        else:
            _id = "_".join([node_name, interface])
            _label = interface
            _parent = node_name
        if _id in id_list:
            pass
        else:
            new_node = {
                "data": {
                    "id": _id,
                    "label": _label,
                    "parent": _parent,
                },
                "classes": "rectangle"
            }
            node_list.append(new_node)
        return node_list

    def _update_edge_list(self, edge_list, source_id, target_id):
        pass

    def _generate_net_json(self, path_obj_list):
        node_list = []
        edge_list = []
        node_json = "/".join([self.output_dir, self.node_json])
        node_json_path = pathlib.Path(node_json)
        edge_json = "/".join([self.output_dir, self.edge_json])
        edge_json_path = pathlib.Path(edge_json)
        for path_obj in path_obj_list:
            try:
                node_name = path_obj.stem
                node_list = self._update_node_list(
                    node_list=node_list,
                    node_name=node_name,
                    interface=None
                )
                with open(path_obj) as f:
                    load_data = json.load(f)
                for interface, target_info in load_data.items():
                    source_id = "_".join([node_name, interface])
                    _target = target_info[0]
                    target_id = "_".join([
                        _target.get("remote_system_name"),
                        _target.get("remote_port_description"),
                    ])
                    node_list = self._update_node_list(
                        node_list=node_list,
                        node_name=node_name,
                        interface=interface
                    )
                    edge_list = self._update_edge_list(
                        edge_list=edge_list,
                        source_id=source_id,
                        target_id=target_id
                    )
            except OSError as e:
                logger.error(str(e))
        node_json_path.write_text(json.dumps(node_list, indent=2))
        edge_json_path.write_text(json.dumps(edge_list, indent=2))

    def run(self):
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
