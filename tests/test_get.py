import pytest
from curl_cffi import requests
from importlib import import_module
from finary_uapi.signin import signin
from finary_uapi.auth import prepare_session
from finary_uapi.securities import get_securities


def test_signin() -> None:
    """test signin"""
    result = signin()
    assert result["response"]
    assert result["response"]["status"] == "complete"


@pytest.fixture
def session() -> requests.Session:
    return prepare_session()


@pytest.mark.parametrize(
    "module_name, function_name, args, result_count",
    [
        ("bank_account_types", "", {"type": "invest"}, 1),
        ("bank_account_types", "", {"type": "cash"}, 1),
        ("crypto_chains", "", {}, 1),
        ("currencies", "", {"type": "crypto", "query": "BTC"}, 1),
        ("currencies", "", {"type": "fiat", "query": "USD"}, 1),
        ("generic_asset_categories", "", {}, 1),
        ("institutions", "", {"name": "cred"}, 1),
        ("precious_metals", "", {"query": "or"}, 1),
        ("scpis", "", {"query": "corum"}, 1),
        ("securities", "", {"query": "GOOG"}, 1),
        ("user_cryptos", "", {}, 1),
        ("user_fonds_euro", "", {}, 1),
        ("user_generic_assets", "", {}, 1),
        (
            "user_holdings_accounts",
            "get_holdings_accounts",
            {},
            1,
        ),  # TODO change name and add _user_
        ("user_me", "", {}, 1),
        ("user_me", "get_user_me_institution_connections", {}, 1),
        ("user_me", "get_user_me_organizations", {}, 1),
        ("user_me", "get_user_me_sharing_links", {}, 1),
        ("user_me", "get_user_me_subscription_details", {}, 1),
        ("user_portfolio", "get_portfolio_crowdlendings", {}, 1),
        ("user_portfolio", "get_portfolio_crowdlendings_distribution", {}, 1),
        ("user_portfolio", "get_portfolio_cryptos", {}, 1),
        ("user_portfolio", "get_portfolio_cryptos_distribution", {}, 1),
        ("user_portfolio", "get_portfolio_investments", {}, 1),
        ("user_portfolio", "get_portfolio_investments_dividends", {}, 1),
        ("user_portfolio", "get_portfolio_investments_transactions", {}, 0),
        ("user_portfolio", "get_portfolio_checking_accounts_transactions", {}, 0),
        ("user_portfolio", "get_portfolio_credit_accounts_transactions", {}, 0),
        ("user_precious_metals", "", {}, 1),
        ("user_real_estates", "", {}, 1),
        ("user_scpis", "", {}, 1),
        ("user_securities", "", {}, 1),
        ("user_startups", "", {}, 1),
        ("watches", "", {"query": "rolex"}, 1),
    ],
)
def test_generic_test(
    session: requests.Session,
    module_name: str,
    function_name: str,
    args,
    result_count: int,
) -> None:
    if not function_name:
        function_name = f"get_{module_name}"
    module = import_module(f"finary_uapi.{module_name}")
    bar = getattr(module, function_name)
    result = bar(session, **args)
    assert result
    assert result["message"] == "OK"
    assert result["error"] is None
    if result_count > 0:
        assert len(result["result"]) > 0


def test_get_security_error(session: requests.Session) -> None:
    securities = get_securities(session, "US5949181045XDE")
    assert securities
    assert securities["result"] == []
