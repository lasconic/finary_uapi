import pytest
import requests
from finary_uapi.bank_account_types import get_bank_account_type_per_name
from finary_uapi.currencies import get_cryptocurrency_by_code
from finary_uapi.signin import signin
from finary_uapi.auth import prepare_session
from finary_uapi.user_holdings_accounts import get_holdings_account_per_name_or_id
from finary_uapi.user_cryptos import get_user_crypto_by_code
from finary_uapi.securities import guess_security


def test_signin() -> None:
    """test signin"""
    result = signin()
    assert result["message"] == "Created"
    assert result["error"] is None


@pytest.fixture
def session() -> requests.Session:
    return prepare_session()


@pytest.mark.parametrize(
    "type, name, display_name",
    [
        ("invest", "lifeinsurance", "Assurance vie"),
        ("cash", "checking", "Compte courant"),
    ],
)
def test_get_bank_account_type_per_name(
    session: requests.Session, type: str, name: str, display_name: str
) -> None:
    account = get_bank_account_type_per_name(session, type, display_name)
    assert account["name"] == name
    assert account["display_name"] == display_name


def test_get_bank_account_type_per_name_error(session: requests.Session) -> None:
    account = get_bank_account_type_per_name(session, "cash", "foo")
    assert not account


@pytest.mark.parametrize(
    "code, name",
    [
        ("BTC", "Bitcoin"),
        ("SushiToken", "SushiToken"),
    ],
)
def test_get_cryptocurrency_by_code(
    session: requests.Session, code: str, name: str
) -> None:
    crypto = get_cryptocurrency_by_code(session, code)
    assert crypto
    assert crypto["name"] == name


def test_get_cryptocurrency_by_code_error(session: requests.Session) -> None:
    crypto = get_cryptocurrency_by_code(session, "foobar")
    assert not crypto


@pytest.mark.parametrize(
    "name_id",
    [
        ("Assurance CM"),
        ("90e407ad-fb28-48e1-a0c9-742fd9e4913d"),
    ],
)
def test_get_holdings_account_per_name_or_id(
    session: requests.Session, name_id: str
) -> None:
    account = get_holdings_account_per_name_or_id(session, name_id)
    assert account["name"] == name_id or account["id"] == name_id


def test_get_user_crypto_by_code(session: requests.Session) -> None:
    crypto = get_user_crypto_by_code(
        session, "BTC", "4492f61e-2f89-4ace-bc55-f9358cbcbd82"
    )
    assert crypto["quantity"] == 1


def test_get_user_crypto_by_code_error(session: requests.Session) -> None:
    crypto = get_user_crypto_by_code(
        session, "foo", "4492f61e-2f89-4ace-bc55-f9358cbcbd82"
    )
    assert crypto == {}


@pytest.mark.parametrize(
    "isin_code, description, currency, check",
    [
        ("FR0000120271", "TotalEnergies", "EUR", "TTE"),
        ("NONEXISTENT", "NONEXISTENT", "EUR", "error"),
        ("0P00000H2W", "Regard", "EUR", "0P00000H2W"),
        ("0P00000H2W", "", "EUR", "0P00000H2W"),
        ("0P00000H2W", "ZZZZZ", "EUR", "error"),
        ("TTE", "TotalEnergies", "EUR", "TTE"),
        ("FR0000120271", "", "EUR", "TTE"),
        ("FR0000120271", "ZZZZZ", "EUR", "error"),
        ("wayfair", "", "GBP", "error"),
    ],
)
def test_guess_security(
    session: requests.Session,
    isin_code: str,
    description: str,
    currency: str,
    check: str,
) -> None:
    security = {}
    security["isin_code"] = isin_code
    security["description"] = description
    security["currency"] = currency
    security = guess_security(session, security)
    if check == "error":
        assert security == {}
    else:
        assert security
        assert security["symbol"] == check
        assert security["currency"]["code"] == currency  # type: ignore
