from urllib import request
from .constants import API_ROOT
import requests
from .utils import get_and_print

fe_url = f"{API_ROOT}/users/me/fonds_euro"

def get_user_fonds_euro(session: requests.Session):
    return get_and_print(session, fe_url)