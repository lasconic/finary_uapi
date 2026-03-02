from curl_cffi import requests
from typing import Any

from .constants import API_ROOT
from .utils import get_and_print


def get_organization_investments(session: requests.Session, org_id: str) -> Any:
    """Aggregated portfolio view — result is a dict, not a list."""
    url = f"{API_ROOT}/organizations/{org_id}/portfolio/investments"
    return get_and_print(session, url)


def get_organization_securities(session: requests.Session, org_id: str) -> Any:
    url = f"{API_ROOT}/organizations/{org_id}/securities"
    return get_and_print(session, url)


def get_organization_cryptos(session: requests.Session, org_id: str) -> Any:
    url = f"{API_ROOT}/organizations/{org_id}/cryptos"
    return get_and_print(session, url)


def get_organization_fonds_euro(session: requests.Session, org_id: str) -> Any:
    url = f"{API_ROOT}/organizations/{org_id}/fonds_euro"
    return get_and_print(session, url)


def get_organization_real_estates(session: requests.Session, org_id: str) -> Any:
    url = f"{API_ROOT}/organizations/{org_id}/real_estates"
    return get_and_print(session, url)


def get_organization_scpis(session: requests.Session, org_id: str) -> Any:
    url = f"{API_ROOT}/organizations/{org_id}/scpis"
    return get_and_print(session, url)


def get_organization_holdings_accounts(session: requests.Session, org_id: str) -> Any:
    url = f"{API_ROOT}/organizations/{org_id}/holdings_accounts"
    return get_and_print(session, url)
