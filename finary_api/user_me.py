import json
import requests
from .constants import API_ROOT


def get_user_me(session: requests.Session) -> str:
    url = f"{API_ROOT}/users/me"
    x = session.get(url)
    print(json.dumps(x.json(), indent=4))
    return str(x.json())


def get_user_me_institution_connections(session: requests.Session) -> str:
    url = f"{API_ROOT}/users/me/institution_connections/details"
    x = session.get(url)
    print(json.dumps(x.json(), indent=4))
    return str(x.json())
