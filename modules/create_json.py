from __future__ import annotations

import functools
import json
import pathlib
import sys
from logging import getLogger

import click
from typing import Optional, Union, Dict, List

logger = getLogger(__name__)

PATH_OBJ = pathlib.Path
PATH_OBJ_LIST = List[PATH_OBJ]

DATA = Dict[str, str]
NODE = Dict[str, Union[str, DATA]]
NODE_LIST = List[NODE]
EDGE = Dict[str, DATA]
EDGE_LIST = List[EDGE]


class Runner:

    def __init__(self, input_dir: str, output_dir: str) -> None:
        self.input_dir: PATH_OBJ = pathlib.Path(input_dir)
        self.node_json: str = f"{output_dir}/node.json"
        self.edge_json: str = f"{output_dir}/edge.json"
        self.node_list: NODE_LIST = []
        self.edge_list: EDGE_LIST = []
        self.id_list: List[str] = []
        self.source_list: List[str] = []
        self.target_list: List[str] = []

    def _glob_dir(self, regex: str = None) -> PATH_OBJ_LIST:
        """指定ディレクトリからファイル一覧を取得する."""
        if regex is None:
            _glob_regex = "[!.]*"
        else:
            _glob_regex = regex
        try:
            obj = self.input_dir.glob(_glob_regex)
            path_obj_list = list(p for p in obj if p.is_file())
        except OSError as e:
            msg = "Cannot load file: %s" % str(e)
            logger.error(msg, exc_info=True)
            raise Exception
        return path_obj_list

    def _update_node_list(self, node_name: str, interface: str, option=None) -> None:
        _data: DATA = {
            "id": f"{node_name}_{interface}",
            "label": interface,
            "parent": node_name
        }
        if option is not None:
            _data.update(option)
        new_node: NODE = {
            "data": _data,
            "classes": "rectangle",
            "group": "nodes",
        }

        # Append node if not exist.
        if node_name not in self.id_list:
            parent_node: NODE = new_node.copy()
            parent_node["data"] = {
                "id": node_name,
                "label": node_name,
                "parent": None,
            }
            self.node_list.append(parent_node)
            self.id_list.append(node_name)

        # Append interface if not exist.
        if _data["id"] not in self.id_list:
            self.node_list.append(new_node)
            self.id_list.append(_data["id"])

    def _update_edge_list(self, source_id: str, target_id: str, option=None) -> None:
        _data = {"source": source_id, "target": target_id}
        if option is not None:
            _data.update(option)
        new_edge = {"data": _data, "group": "edges"}

        if source_id in self.source_list and target_id in self.target_list:
            pass  # edge_list has already `new_edge`.
        elif source_id in self.target_list and target_id in self.source_list:
            pass  # edge_list has already `new_edge` by reverse.
        else:
            self.edge_list.append(new_edge)
            self.source_list.append(source_id)
            self.target_list.append(target_id)

    def _generate_net_json(self, lldp_file_list: PATH_OBJ_LIST) -> None:
        p_node_json: PATH_OBJ = pathlib.Path(self.node_json)
        p_edge_json: PATH_OBJ = pathlib.Path(self.edge_json)

        for lldp_file in lldp_file_list:
            print(f"Loading {lldp_file}")
            try:
                with open(lldp_file) as f:
                    load_data = json.load(f)

                source_name = lldp_file.stem
                for source_interface, target_info in load_data.items():
                    source_id = f"{source_name}_{source_interface}"

                    try:
                        target_name = target_info[0].get("remote_system_name")
                        target_interface = target_info[0]["remote_port_description"]
                    except KeyError:
                        target_name = target_info[0]["hostname"]
                        target_interface = target_info[0]["port"]
                    except Exception:
                        raise IndexError
                    target_id = f"{target_name}_{target_interface}"

                    # Node update for source device.
                    print(f" Updating Node: {source_name}")
                    self._update_node_list(
                        node_name=source_name,
                        interface=source_interface,
                        option=None,  # add optional info. future release.
                    )

                    # Node update for target device.
                    print(f" Updating Node: {target_name}")
                    self._update_node_list(
                        node_name=target_name,
                        interface=target_interface,
                        option=None,  # add optional info. future release.
                    )

                    # Edge update
                    print(f" Updating Edge: {source_id},{target_id}")
                    self._update_edge_list(
                        source_id=source_id,
                        target_id=target_id,
                        option=None,  # add optional info. future release.
                    )
            except OSError as e:
                logger.error(str(e))
            except IndexError as e:
                logger.error(str(e))
        p_node_json.write_text(json.dumps(self.node_list, indent=2))
        p_edge_json.write_text(json.dumps(self.edge_list, indent=2))

    def run(self) -> None:
        try:
            print("Loading lldp files.")
            lldp_file_list: PATH_OBJ_LIST = self._glob_dir()

            print("Generating json files.")
            self._generate_net_json(lldp_file_list)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            sys.exit(1)
        else:
            print("Generating json files successfuly.")


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
