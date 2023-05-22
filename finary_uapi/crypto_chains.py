from typing import Any
import requests

from .utils import get_and_print
from .constants import API_ROOT


def get_crypto_chains(session: requests.Session) -> Any:
    url = f"{API_ROOT}/crypto/chains"
    return get_and_print(session, url)
