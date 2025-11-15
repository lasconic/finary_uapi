from curl_cffi import requests
from .utils import get_and_print_autocomplete, get_and_print_most_popular
from .constants import API_ROOT

scpis_url = f"{API_ROOT}/scpis"


def get_scpis(session: requests.Session, query: str):
    """
    This function will get a list of scpis to be added,
    and not the user scpis, see user_scpis for the scpis owned by the user
    """
    return get_and_print_autocomplete(session, scpis_url, query)


def get_most_popular_watches(session: requests.Session, country: str, limit: int):
    """
    This function will get a list of `limit` popular scpis for a given country,
    a user watch can be added as a generic asset
    """
    get_and_print_most_popular(session, scpis_url, country=country, limit=limit)
