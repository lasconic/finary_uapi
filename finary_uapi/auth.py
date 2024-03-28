import http.cookiejar
import json
import httpx
from httpx import Headers
from .constants import APP_ROOT, CLERK_ROOT, COOKIE_FILENAME, JWT_FILENAME
from . import __version__ as FINARY_UAPI_VERSION


def prepare_session() -> httpx.Client:
    s = httpx.Client(timeout=10.0)
    file_name = JWT_FILENAME

    with open(file_name, "r") as json_file:
        data = json.load(json_file)

    # Extract the session_token from the loaded data
    session_token = data.get("session_token")
    session_id = data.get("session_id")

    # refresh the token if needed
    s.headers.clear()

    saved_cookie = s.cookies
    cookie_jar_file = http.cookiejar.MozillaCookieJar(COOKIE_FILENAME)
    cookie_jar_file.load(COOKIE_FILENAME)
    s.cookies = cookie_jar_file  # type: ignore

    tokens_url = f"{CLERK_ROOT}/v1/client/sessions/{session_id}/tokens"
    headers = Headers(
        {
            "Origin": f"{APP_ROOT}",
            "Referer": f"{APP_ROOT}",
            "User-Agent": f"finary_uapi {FINARY_UAPI_VERSION}",
        }
    )
    s.headers = headers
    x = s.post(tokens_url, headers=headers)
    if x.status_code == 200:
        session_token = x.json()["jwt"]
        data = {"session_token": session_token, "session_id": session_id}
        with open(JWT_FILENAME, "w") as json_file:
            json.dump(data, json_file)

    s.cookies = saved_cookie
    s.headers.update({"authorization": f"Bearer {session_token}"})

    return s
