import pytest
from finary_uapi.sharing import get_sharing


@pytest.mark.parametrize(
    "sharing_code_url",
    [
        ("https://app.finary.com/share/32e83f4b62f1ac2fbd63/checking-accounts"),
        ("https://app.finary.com/share/32e83f4b62f1ac2fbd63"),
        ("32e83f4b62f1ac2fbd63"),
    ],
)
def test_get_sharing(sharing_code_url: str) -> None:
    result = get_sharing(sharing_code_url)
    assert result["message"] == "OK"
    assert result["error"] is None
    assert len(result["result"]) > 0


def test_get_sharing_not_found() -> None:
    result = get_sharing("32e83f4b62f1ac2fbd6")
    assert result["message"] == "Not Found"
    assert result["error"] is None
    assert result["result"] is None


def test_get_sharing_not_valid() -> None:
    result = get_sharing("32e83f4b62f1ac2fbd6!")
    assert result == {}


def test_get_sharing_forbidden() -> None:
    result = get_sharing("https://app.finary.com/v2/share/2245fc1afbec337108d0")
    assert result["message"] == "Forbidden"
    assert result["error"]
    assert result["error"]["code"] == "REQUEST_FORBIDDEN"
    assert result["result"] is None


def test_get_sharing_secret() -> None:
    result = get_sharing(
        "https://app.finary.com/v2/share/2245fc1afbec337108d0", "3rIo8g"
    )
    assert result["message"] == "OK"
    assert result["error"] is None
    assert len(result["result"]) > 0
