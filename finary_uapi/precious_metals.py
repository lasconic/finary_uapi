from curl_cffi import requests

from finary_uapi.utils import get_and_print_autocomplete, get_and_print_most_popular
from .constants import API_ROOT

precious_metals_url = f"{API_ROOT}/precious_metals"


def get_precious_metals(session: requests.Session, query: str):
    """
    This function will get a list of metals to be added,
    and not the user metals, see views/commodities for the user metals
    """
    return get_and_print_autocomplete(session, precious_metals_url, query)


def get_most_popular_precious_metals(
    session: requests.Session, country: str, limit: int
):
    """
    This function will get a list of `limit` popular precious_metals for a given country,
    a user watch can be added as a generic asset
    """
    get_and_print_most_popular(
        session, precious_metals_url, country=country, limit=limit
    )
