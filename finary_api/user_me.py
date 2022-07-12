from typing import Any
import requests

from .utils import get_and_print
from .constants import API_ROOT


def get_user_me(session: requests.Session) -> Any:
    url = f"{API_ROOT}/users/me"
    return get_and_print(session, url)


def get_user_me_institution_connections(session: requests.Session) -> Any:
    url = f"{API_ROOT}/users/me/institution_connections/details"
    return get_and_print(session, url)
