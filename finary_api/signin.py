import http.cookiejar
import json
import logging
import os
from typing import Any
import requests
from .constants import API_ROOT, CREDENTIAL_FILE, COOKIE_FILENAME


def signin(otp_code: str = "") -> Any:
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
        "Content-Type": "application/json; charset=utf-8",
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
    elif x.status_code == 202:  # 2fa
        result = x.json()
        otp_relay_token = result["result"]["otp_relay_token"]
        if not otp_code:
            otp_code = input("Enter 2FA code:")
        data = {}
        data["device_id"] = credentials["device_id"]
        data["otp_code"] = otp_code
        data["otp_relay_token"] = otp_relay_token
        data_json = json.dumps(data)
        headers["Content-Length"] = f"{len(data_json)}"
        x = session.post(signin_url, data=data_json, headers=headers)
        if x.status_code == 201:
            cookie_jar_file.save()
            logging.info("Sign in OK")
            obj = json.loads(x.content)
            logging.debug(json.dumps(obj, indent=4))
        else:
            logging.info(f"Error 2fa [{x.status_code}]")
    else:
        logging.info(f"Error [{x.status_code}]")
    return x.json()
