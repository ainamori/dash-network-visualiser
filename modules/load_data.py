from __future__ import annotations

import os
import json
import pathlib
from logging import getLogger
# from typing import Optional, Dict, Any
# from modules.data_type import DATA, NODE_LIST, NODE, EDGE_LIST, EDGE, LOAD_DATA, STYLES
from modules.data_type import LOAD_DATA, STYLES
from modules.create_json import CreateJson

logger = getLogger(__name__)


class LoadingData:

    def __init__(self) -> None:
        self.data_dir: str = "data"
        self.node_json = os.path.join(*[self.data_dir, "node.json"])
        self.edge_json = os.path.join(*[self.data_dir, "edge.json"])
        self.styles: str = "style/styles.json"
        self._check_data_dir()
        self.create_json = CreateJson("./data")

    def _check_data_dir(self):
        if not pathlib.Path(self.data_dir).exists():
            raise OSError(f"data dir:'{self.data_dir}' is not found.")

    def loading_styles(self) -> STYLES:
        styles: STYLES = {}
        print("Loading styles.")
        with open(self.styles, 'r') as f:
            styles = json.load(f)
        return styles

    def _load_data(self) -> LOAD_DATA:
        load_data: LOAD_DATA = []
        load_data = self.create_json.data_dumper()
        return load_data

    def _load_json(self) -> LOAD_DATA:
        load_data: LOAD_DATA = []
        try:
            print("Loading node data.")
            with open(self.node_json, 'r') as f:
                node_data = json.load(f)

            print("Loading edge data.")
            with open(self.edge_json, 'r') as f:
                edge_data = json.load(f)

            load_data.extend(node_data)
            load_data.extend(edge_data)
        except OSError as e:
            print(f"Skip loding json file. Loading file: {str(e)}")
        except Exception as e:
            print(f"Skip loding json file. Unknown Error: {str(e)}")
        finally:
            return load_data

    def loading_data(self) -> LOAD_DATA:
        load_data: LOAD_DATA = []
        if pathlib.Path(self.node_json).exists() and pathlib.Path(self.edge_json).exists():
            load_data = self._load_json()
        else:
            load_data = self._load_data()
        return load_data
