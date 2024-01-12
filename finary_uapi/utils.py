import json
import logging
import requests


def get_and_print(session: requests.Session, url: str):
    x = session.get(url)
    result = {}
    if x.status_code in [200, 304]:
        result = x.json()
        logging.debug(json.dumps(x.json(), indent=4))
    else:
        logging.debug(f"Status code : [{x.status_code}]")
    return result
