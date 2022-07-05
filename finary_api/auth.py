import http.cookiejar
import requests
from .constants import COOKIE_FILENAME


def prepare_session() -> requests.Session:
    s = requests.Session()
    cookie_jar_file = http.cookiejar.MozillaCookieJar(COOKIE_FILENAME)
    cookie_jar_file.load(COOKIE_FILENAME)
    s.cookies = cookie_jar_file  # type: ignore
    return s
