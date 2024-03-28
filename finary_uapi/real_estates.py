import json
import logging
import httpx
from .constants import API_ROOT


def get_real_estates_placeid(session: httpx.Client, search_str: str):
    real_estates_url = f"{API_ROOT}/real_estates/autocomplete?query={search_str}"
    x = session.get(real_estates_url)
    logging.debug(json.dumps(x.json(), indent=4))
    data = x.json()

    return data["result"][0]["place_id"]
