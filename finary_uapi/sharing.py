import json
import logging
import requests
from typing import Any

from .constants import API_ROOT


def get_sharing(sharing_code_url: str = "", secret_code: str = "") -> Any:
    sharing_code = sharing_code_url.strip()
    if sharing_code.startswith("http"):
        s_array = sharing_code.split("/")
        if "share" in s_array:
            sharing_code = s_array[s_array.index("share") + 1]
    if not sharing_code.isalnum():
        logging.debug("sharing code is not well formatted")
        return {}
    sharing_url = f"{API_ROOT}/sharing/{sharing_code}"
    session = requests.Session()
    params = {}
    if secret_code:
        params["code"] = secret_code
    x = session.get(sharing_url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
