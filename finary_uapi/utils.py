import json
import logging
import requests
from .constants import CREDENTIAL_FILE, API_ROOT

def get_and_print(session: requests.Session, url: str):
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()

def get_real_estates_placeid(session: requests.Session, search_str: str):
    Finary_Req_url = f"{API_ROOT}/real_estates/autocomplete?query={search_str}"
    x = session.get(Finary_Req_url)
    logging.debug(json.dumps(x.json(), indent=4))
    data = x.json()
    return data['result'][0]['place_id']