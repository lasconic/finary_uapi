from curl_cffi import requests
from .constants import API_ROOT
from .utils import get_and_print


def get_user_startups(session: requests.Session):
    url = f"{API_ROOT}/users/me/startups"
    return get_and_print(session, url)
