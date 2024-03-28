import json
import logging
import httpx


def get_and_print(session: httpx.Client, url: str):
    x = session.get(url)
    result = {}
    if x.status_code in [200, 304]:
        result = x.json()
        logging.debug(json.dumps(x.json(), indent=4))
    else:
        logging.debug(f"Status code : [{x.status_code}]")
    return result
