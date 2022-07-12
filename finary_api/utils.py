import json
import logging
import requests


def get_and_print(session: requests.Session, url: str):
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
