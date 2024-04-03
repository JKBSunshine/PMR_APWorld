import os
import orjson
import pkgutil
from typing import Dict, Any, Union, List


def data_path(*args):
    return os.path.join(os.path.dirname(__file__), 'data', *args)


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))
