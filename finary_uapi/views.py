import requests
from .constants import API_ROOT
from .utils import get_and_print

views_url = f"{API_ROOT}/users/me/views"


def get_insights(session: requests.Session):
    url = f"{views_url}/insights"
    return get_and_print(session, url)


def get_loans(session: requests.Session):
    url = f"{views_url}/loans"
    return get_and_print(session, url)
