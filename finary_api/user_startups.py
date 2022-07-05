import json
import logging
import requests
from .constants import API_ROOT


def get_startups(session: requests.Session):
    url = f"{API_ROOT}/users/me/wealth/startups"
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
