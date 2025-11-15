import json
import logging
from curl_cffi import requests


def get_and_print(session: requests.Session, url: str):
    x = session.get(url)
    result = {}
    if x.status_code in [200, 304]:
        result = x.json()
        logging.debug(json.dumps(x.json(), indent=4))
    else:
        logging.debug(f"Status code : [{x.status_code}]")
    return result


def get_and_print_autocomplete(session: requests.Session, root_url: str, query: str):
    url = f"{root_url}/autocomplete"
    params = {}
    if query:
        params["query"] = query

    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_and_print_most_popular(
    session: requests.Session, root_url: str, country: str = "FR", limit: int = 20
):
    """
    This function will get a list of `limit` popular watches for a given country,
    a user watch can be added as a generic asset
    """
    url = f"{root_url}/most_popular"
    params = {"limit": limit, "country": country}
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
