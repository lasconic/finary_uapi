import json
import requests
from .constants import API_ROOT

portfolio_api = f"{API_ROOT}/users/me/portfolio"


def get_and_print(session: requests.Session, url: str):
    x = session.get(url)
    print(json.dumps(x.json(), indent=4))
    return x.json()


def get_portfolio(session: requests.Session, type: str):
    url = f"{portfolio_api}/{type}"
    return get_and_print(session, url)


def get_portfolio_cryptos(session: requests.Session):
    return get_portfolio(session, "cryptos")


def get_portfolio_investments(session: requests.Session):
    return get_portfolio(session, "investments")
