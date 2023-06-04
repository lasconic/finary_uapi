import pytest
import requests
from importlib import import_module
from finary_uapi.signin import signin
from finary_uapi.auth import prepare_session
from finary_uapi.securities import get_securities


def test_signin() -> None:
    """test signin"""
    result = signin()
    assert result["message"] == "Created"
    assert result["error"] is None


@pytest.fixture
def session() -> requests.Session:
    return prepare_session()


@pytest.mark.parametrize(
    "module_name, function_name, args",
    [
        ("bank_account_types", "", {"type": "invest"}),
        ("bank_account_types", "", {"type": "cash"}),
        ("crypto_chains", "", {}),
        ("currencies", "", {"type": "crypto", "query": "BTC"}),
        ("currencies", "", {"type": "fiat", "query": "USD"}),
        ("generic_asset_categories", "", {}),
        ("institutions", "", {"name": "cred"}),
        ("precious_metals", "", {"query": "or"}),
        ("scpis", "", {"query": "corum"}),
        ("securities", "", {"query": "GOOG"}),
        ("user_cryptos", "", {}),
        ("user_fonds_euro", "", {}),
        ("user_generic_assets", "", {}),
        (
            "user_holdings_accounts",
            "get_holdings_accounts",
            {},
        ),  # TODO change name and add _user_
        ("user_me", "", {}),
        ("user_me", "get_user_me_institution_connections", {}),
        ("user_me", "get_user_me_sharing_links", {}),
        ("user_me", "get_user_me_subscription_details", {}),
        ("user_portfolio", "get_portfolio_crowdlendings", {}),
        ("user_portfolio", "get_portfolio_crowdlendings_distribution", {}),
        ("user_portfolio", "get_portfolio_cryptos", {}),
        ("user_portfolio", "get_portfolio_cryptos_distribution", {}),
        ("user_portfolio", "get_portfolio_investments", {}),
        ("user_precious_metals", "", {}),
        ("user_real_estates", "", {}),
        ("user_scpis", "", {}),
        ("user_securities", "", {}),
        ("user_startups", "", {}),
        ("views", "get_dashboard", {"type": "net", "period": "all"}),
        ("views", "get_dashboard", {"type": "gross", "period": "all"}),
        ("views", "get_dashboard", {"type": "finary", "period": "all"}),
        ("views", "get_portfolio", {"period": "all"}),
        ("views", "get_savings_accounts", {"period": "all"}),
        ("views", "get_checking_accounts", {"period": "all"}),
        ("views", "get_other_assets", {"period": "all"}),
        ("views", "get_fonds_euro", {"period": "all"}),
        ("views", "get_real_estates", {"period": "all"}),
        ("views", "get_commodities", {"period": "all"}),
        ("views", "get_insights", {}),
        ("views", "get_fees", {}),
        ("views", "get_loans", {}),
        ("views", "get_credit_accounts", {}),
        ("watches", "", {"query": "rolex"}),
    ],
)
def test_generic_test(
    session: requests.Session, module_name: str, function_name: str, args
) -> None:
    if not function_name:
        function_name = f"get_{module_name}"
    module = import_module(f"finary_uapi.{module_name}")
    bar = getattr(module, function_name)
    result = bar(session, **args)
    assert result["message"] == "OK"
    assert result["error"] is None
    assert len(result["result"]) > 0


def test_get_security_error(session: requests.Session) -> None:
    securities = get_securities(session, "US5949181045")
    assert securities
    assert securities["result"] == []
