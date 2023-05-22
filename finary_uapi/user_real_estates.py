import requests
from .constants import API_ROOT
from .utils import get_and_print


def get_user_real_estates(session: requests.Session):
    url = f"{API_ROOT}/users/me/real_estates"
    return get_and_print(session, url)
