import http.cookiejar
import json
import logging
import os
from typing import Any
import requests
from .constants import API_ROOT, CREDENTIAL_FILE, COOKIE_FILENAME


def signin() -> Any:
    signin_url = f"{API_ROOT}/auth/signin"

    # load from environment variables
    email = os.environ.get("FINARY_EMAIL")
    password = os.environ.get("FINARY_PASSWORD")

    if email and password:
        credentials = {
            "email": email,
            "password": password,
        }
    else:  # load from credentials.json
        cred_file = open(CREDENTIAL_FILE, "r")
        credentials = json.load(cred_file)

    credentials[
        "device_id"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"  # noqa

    credentials_json = json.dumps(credentials)

    headers = {
        "Content-Length": f"{len(credentials_json)}",
        "Content-Type": "application/json",
    }

    session = requests.Session()
    cookie_jar_file = http.cookiejar.MozillaCookieJar(COOKIE_FILENAME)
    session.cookies = cookie_jar_file  # type: ignore
    x = session.post(signin_url, data=credentials_json, headers=headers)
    logging.debug(x.status_code)
    if x.status_code == 201:
        cookie_jar_file.save()
        logging.info("Sign in OK")
        obj = json.loads(x.content)
        logging.debug(json.dumps(obj, indent=4))
        return x.json()
    else:
        logging.info(f"error [{x.status_code}]")
