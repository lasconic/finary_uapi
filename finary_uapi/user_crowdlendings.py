import json
import logging
import requests
from .constants import API_ROOT

CROWDLENDINGS_URL = f"{API_ROOT}/users/me/crowdlendings"

def get_user_crowdlendings(session: requests.Session):
    x = session.get(CROWDLENDINGS_URL)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def delete_user_crowdlending(session: requests.Session, crowdlending_id):
    """
    crowdlending_id is the numerical id of the crowdlending for this user, as provided by GET
    """
    url = f"{CROWDLENDINGS_URL}/{crowdlending_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def add_user_crowdlending(
    session: requests.Session,
    account_id:str,
    annual_yield: float,
    currency_code: str,
    current_price:  float,
    initial_investment: float,
    month_duration: int,
    name: str,
    start_date: str
):
    """
    
    """
    data = {}
    data["account"] = {"id": account_id}
    data["annual_yield"] = annual_yield
    data["currency"] = {"code": currency_code}
    data["current_price"] = current_price
    data["initial_investment"] = initial_investment
    data["month_duration"] = month_duration
    data["name"] = name
    data["start_date"] = start_date
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(CROWDLENDINGS_URL, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()