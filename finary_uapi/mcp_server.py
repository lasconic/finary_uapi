"""MCP server exposing Finary API operations as tools."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .auth import prepare_session
from .crypto_chains import get_crypto_chains
from .currencies import get_currencies
from .generic_asset_categories import get_generic_asset_categories
from .institutions import get_institutions
from .precious_metals import get_precious_metals
from .scpis import get_scpis
from .securities import get_securities
from .signin import signin
from .user_cryptos import get_user_cryptos
from .user_fonds_euro import get_user_fonds_euro
from .user_holdings_accounts import get_holdings_account_per_name_or_id, get_holdings_accounts
from .user_me import get_family_org_id, get_user_me, get_user_me_institution_connections, get_user_me_organizations
from .user_organizations import (
    get_organization_cryptos,
    get_organization_fonds_euro,
    get_organization_holdings_accounts,
    get_organization_investments,
    get_organization_real_estates,
    get_organization_scpis,
    get_organization_securities,
)
from .user_portfolio import (
    get_portfolio_checking_accounts_transactions,
    get_portfolio_credit_accounts_transactions,
    get_portfolio_crowdlendings,
    get_portfolio_crowdlendings_distribution,
    get_portfolio_cryptos_distribution,
    get_portfolio_investments,
    get_portfolio_investments_dividends,
    get_portfolio_investments_transactions,
    get_portfolio_timeseries,
)
from .user_real_estates import get_user_real_estates
from .user_scpis import get_user_scpis
from .user_securities import get_user_securities
from .user_startups import get_user_startups
from .watches import get_watches


mcp = FastMCP("finary-uapi")


def _session():
    return prepare_session()


def _resolve_org_id(session: Any, org_id: str) -> str:
    if org_id == "family":
        family_org_id = get_family_org_id(session)
        if family_org_id is None:
            raise ValueError("No family organization found for this account")
        return family_org_id
    return org_id


def _portfolio_or_org(
    session: Any,
    org_id: str,
    personal_fn: Any,
    org_fn: Any,
) -> Any:
    if org_id:
        return org_fn(session, _resolve_org_id(session, org_id))
    return personal_fn(session)


@mcp.tool()
def sign_in(mfa_code: str = "", jwt_token: str = "") -> dict[str, Any]:
    """Authenticate and persist JWT for later calls."""
    return signin(otp_code=mfa_code, jwt_token=jwt_token)


@mcp.tool()
def me() -> dict[str, Any]:
    """Get current user profile."""
    return get_user_me(_session())


@mcp.tool()
def institution_connections() -> dict[str, Any]:
    """Get user's institution connections details."""
    return get_user_me_institution_connections(_session())


@mcp.tool()
def organizations() -> dict[str, Any]:
    """Get user's organizations."""
    return get_user_me_organizations(_session())


@mcp.tool()
def holdings_accounts(account_name_or_id: str = "", account_type: str = "", org_id: str = "") -> dict[str, Any]:
    """List holdings accounts, or fetch one by account name/id."""
    session = _session()
    if account_name_or_id:
        return get_holdings_account_per_name_or_id(session, account_name_or_id)
    if org_id:
        return get_organization_holdings_accounts(session, _resolve_org_id(session, org_id))
    return get_holdings_accounts(session, account_type)


@mcp.tool()
def fonds_euro(org_id: str = "") -> dict[str, Any]:
    """Get fonds euro positions, optionally at organization level."""
    session = _session()
    return _portfolio_or_org(session, org_id, get_user_fonds_euro, get_organization_fonds_euro)


@mcp.tool()
def startups() -> dict[str, Any]:
    """Get startup investments."""
    return get_user_startups(_session())


@mcp.tool()
def investments(org_id: str = "") -> dict[str, Any]:
    """Get investments portfolio, optionally at organization level."""
    session = _session()
    return _portfolio_or_org(session, org_id, get_portfolio_investments, get_organization_investments)


@mcp.tool()
def investments_dividends() -> dict[str, Any]:
    """Get dividends from investments portfolio."""
    return get_portfolio_investments_dividends(_session())


@mcp.tool()
def investments_transactions(
    page: int = 1,
    per_page: int = 50,
    account_id: str = "",
    institution_id: str = "",
    query: str = "",
    start_date: str = "",
    end_date: str = "",
    marked: str = "",
) -> dict[str, Any]:
    """Get investment transactions with optional filters."""
    return get_portfolio_investments_transactions(
        _session(),
        page=page,
        per_page=per_page,
        account_id=account_id,
        institution_id=institution_id,
        query=query,
        start_date=start_date,
        end_date=end_date,
        marked=marked,
    )


@mcp.tool()
def checking_accounts_transactions(
    page: int = 1,
    per_page: int = 50,
    account_id: str = "",
    institution_id: str = "",
    query: str = "",
    start_date: str = "",
    end_date: str = "",
    marked: str = "",
) -> dict[str, Any]:
    """Get checking account transactions with optional filters."""
    return get_portfolio_checking_accounts_transactions(
        _session(),
        page=page,
        per_page=per_page,
        account_id=account_id,
        institution_id=institution_id,
        query=query,
        start_date=start_date,
        end_date=end_date,
        marked=marked,
    )


@mcp.tool()
def credit_accounts_transactions(
    page: int = 1,
    per_page: int = 50,
    account_id: str = "",
    institution_id: str = "",
    query: str = "",
    start_date: str = "",
    end_date: str = "",
    marked: str = "",
) -> dict[str, Any]:
    """Get credit account transactions with optional filters."""
    return get_portfolio_credit_accounts_transactions(
        _session(),
        page=page,
        per_page=per_page,
        account_id=account_id,
        institution_id=institution_id,
        query=query,
        start_date=start_date,
        end_date=end_date,
        marked=marked,
    )


@mcp.tool()
def crowdlendings() -> dict[str, Any]:
    """Get crowdlending portfolio."""
    return get_portfolio_crowdlendings(_session())


@mcp.tool()
def crowdlendings_distribution() -> dict[str, Any]:
    """Get crowdlending distribution grouped by account."""
    return get_portfolio_crowdlendings_distribution(_session())


@mcp.tool()
def cryptos(distribution: bool = False, org_id: str = "") -> dict[str, Any]:
    """Get crypto portfolio or crypto distribution."""
    session = _session()
    if distribution:
        return get_portfolio_cryptos_distribution(session)
    return _portfolio_or_org(session, org_id, get_user_cryptos, get_organization_cryptos)


@mcp.tool()
def securities(org_id: str = "") -> dict[str, Any]:
    """Get securities portfolio, optionally at organization level."""
    session = _session()
    return _portfolio_or_org(session, org_id, get_user_securities, get_organization_securities)


@mcp.tool()
def real_estates(org_id: str = "") -> dict[str, Any]:
    """Get real-estates portfolio, optionally at organization level."""
    session = _session()
    return _portfolio_or_org(session, org_id, get_user_real_estates, get_organization_real_estates)


@mcp.tool()
def scpis(org_id: str = "") -> dict[str, Any]:
    """Get SCPI portfolio, optionally at organization level."""
    session = _session()
    return _portfolio_or_org(session, org_id, get_user_scpis, get_organization_scpis)


@mcp.tool()
def timeseries(period: str, series_type: str) -> dict[str, Any]:
    """Get portfolio timeseries for a period and type."""
    return get_portfolio_timeseries(_session(), period=period, type=series_type)


@mcp.tool()
def search(resource: str, query: str) -> dict[str, Any]:
    """Search across finary resources.

    resource: one of crypto_currency, fiat_currency, institutions, precious_metals,
    scpis, securities, watches.
    """
    session = _session()
    if resource == "crypto_currency":
        return get_currencies(session, "crypto", query)
    if resource == "fiat_currency":
        return get_currencies(session, "fiat", query)
    if resource == "institutions":
        return get_institutions(session, query)
    if resource == "precious_metals":
        return get_precious_metals(session, query)
    if resource == "scpis":
        return get_scpis(session, query)
    if resource == "securities":
        return get_securities(session, query)
    if resource == "watches":
        return get_watches(session, query)
    raise ValueError(
        "Invalid resource. Expected one of: crypto_currency, fiat_currency, "
        "institutions, precious_metals, scpis, securities, watches."
    )


@mcp.tool()
def generic_asset_categories() -> dict[str, Any]:
    """Get generic asset categories."""
    return get_generic_asset_categories(_session())


@mcp.tool()
def crypto_chains() -> dict[str, Any]:
    """Get available crypto chains."""
    return get_crypto_chains(_session())


def main() -> None:
    """Run MCP server over stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":  # pragma: nocover
    main()
