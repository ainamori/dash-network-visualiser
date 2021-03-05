from __future__ import annotations

import pathlib
from typing import Union, Dict, List, Any

PATH_OBJ = pathlib.Path
PATH_OBJ_LIST = List[PATH_OBJ]

DATA = Dict[str, str]
NODE = Dict[str, Union[str, DATA]]
NODE_LIST = List[NODE]
EDGE = Dict[str, DATA]
EDGE_LIST = List[EDGE]
LOAD_DATA = List[Union[NODE_LIST, EDGE_LIST]]
STYLES = Dict[str, Any]
