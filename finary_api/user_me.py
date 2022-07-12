import json
import logging
from typing import Any
import requests
from .constants import API_ROOT


def get_user_me(session: requests.Session) -> Any:
    url = f"{API_ROOT}/users/me"
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_user_me_institution_connections(session: requests.Session) -> Any:
    url = f"{API_ROOT}/users/me/institution_connections/details"
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
