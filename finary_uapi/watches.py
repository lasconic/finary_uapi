from curl_cffi import requests

from .utils import get_and_print_autocomplete, get_and_print_most_popular
from .constants import API_ROOT

watches_url = f"{API_ROOT}/watches"


def get_watches(session: requests.Session, query: str):
    """
    This function will get a list of watches to be added,
    a user watch can be added as a generic asset
    """
    return get_and_print_autocomplete(session, watches_url, query)


def get_most_popular_watches(session: requests.Session, country: str, limit: int):
    """
    This function will get a list of `limit` popular watches for a given country,
    a user watch can be added as a generic asset
    """
    get_and_print_most_popular(session, watches_url, country=country, limit=limit)
