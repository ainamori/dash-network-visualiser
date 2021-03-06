from __future__ import annotations

import os
import json
import pathlib
import sys
from logging import getLogger
from typing import Optional, Union, Dict, List
from modules.data_type import PATH_OBJ, PATH_OBJ_LIST
from modules.data_type import LOAD_DATA, DATA, NODE_LIST, NODE, EDGE_LIST, EDGE

logger = getLogger(__name__)


class CreateJson:

    def __init__(self, input_dir: str) -> None:
        self.input_dir: PATH_OBJ = pathlib.Path(input_dir)
        self.data_dir_list: List[str] = [
            "lldp_neighbors",
            "lldp_neighbors_detail",
            "interface",
            "chassis",
            "config",
        ]
        self.node_list: NODE_LIST = []
        self.edge_list: EDGE_LIST = []
        self.id_list: List[str] = []
        self.source_list: List[str] = []
        self.target_list: List[str] = []

    def _glob_dir(self, regex: str = None) -> PATH_OBJ_LIST:
        """指定ディレクトリからファイル一覧を取得する."""
        path_obj_list: Optional[PATH_OBJ_LIST] = []
        if regex is None:
            _glob_regex = "[!.]*"
        else:
            _glob_regex = regex
        try:
            for dir_name in self.data_dir_list:
                dir_path = os.path.join(*[self.input_dir, dir_name])
                obj = pathlib.Path(dir_path).glob(_glob_regex)
                _path_obj_list = list(p for p in obj if p.is_file())
                path_obj_list.extend(_path_obj_list)
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

    def _generate_data(self, file_list: PATH_OBJ_LIST) -> None:

        for _file in file_list:
            print(f"Loading {_file}")
            try:
                with open(_file) as f:
                    load_data = json.load(f)

                source_name = _file.stem
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

    def run(self) -> None:
        print("Loading data files.")
        file_list: PATH_OBJ_LIST = self._glob_dir()
        self._generate_data(file_list)

    def json_dumper(self, output_dir: str) -> int:
        response_code: int = 1
        try:
            self.run()
            node_file: str = os.path.join(*[output_dir, "node.json"])
            edge_file: str = os.path.join(*[output_dir, "edge.json"])
            pathlib.Path(node_file).write_text(json.dumps(self.node_list, indent=2))
            pathlib.Path(edge_file).write_text(json.dumps(self.edge_list, indent=2))
            print("Generating json files successfuly.")
        except OSError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(str(e), exc_info=True)
        else:
            response_code = 0
        finally:
            return response_code

    def data_dumper(self):
        load_data = []
        try:
            self.run()
            load_data.extend(self.node_list)
            load_data.extend(self.edge_list)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            sys.exit(1)
        else:
            return load_data
