from __future__ import annotations

import json
from pathlib import Path
from logging import getLogger
from typing import Optional, Dict, Any
from modules.data_type import DATA, NODE_LIST, NODE, EDGE_LIST, EDGE, LOAD_DATA, STYLES

logger = getLogger(__name__)


class LoadingData:

    def __init__(self) -> None:
        self.data_dir: str = "data/json_data"
        self.node_json: str = f"{self.data_dir}/node.json"
        self.edge_json: str = f"{self.data_dir}/edge.json"
        self.styles_json: str = "style/styles.json"
        self.load_data: LOAD_DATA
        self._check_data_dir

    def _check_data_dir(self):
        if not Path(self.data_dir).exists():
            raise OSError(f"data dir:'{self.data_dir}' is not found.")

    def loading_styles(self) -> STYLES:
        styles: STYLES = {}
        print("Loading styles.")
        with open(self.styles_json, 'r') as f:
            styles = json.load(f)
        return styles

    def _load_lldp_neighbors_detail(self) -> bool:
        """Work in progess"""
        file_exists: bool = False
        return file_exists

    def _load_lldp_neighbors(self) -> bool:
        """Work in progess"""
        file_exists: bool = False
        return file_exists

    def _loading_json(self) -> bool:
        file_exists: bool = False
        self.load_data = []
        try:
            print("Loading node data.")
            with open(self.node_json, 'r') as f:
                node_data = json.load(f)

            print("Loading edge data.")
            with open(self.edge_json, 'r') as f:
                edge_data = json.load(f)

            self.load_data.extend(node_data)
            self.load_data.extend(edge_data)
            file_exists = True
        except OSError as e:
            print(f"Skip loding json file. Loading file: {str(e)}")
        except Exception as e:
            print(f"Skip loding json file. Unknown Error: {str(e)}")
        finally:
            return file_exists

    def loading_data(self) -> LOAD_DATA:
        if self._loading_json():
            return self.load_data
        elif self._load_lldp_neighbors_detail():
            return self.load_data
        elif self._load_lldp_neighbors():
            return self.load_data
        else:
            raise ValueError("No valid data.")
