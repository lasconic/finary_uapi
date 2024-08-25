import logging
import http.cookiejar
import json
import os
from typing import Any
import requests
from .constants import (
    APP_ROOT,
    CLERK_ROOT,
    COOKIE_FILENAME,
    CREDENTIAL_FILE,
    JWT_FILENAME,
)
from . import __version__


def signin(otp_code: str = "") -> Any:
    signin_url = f"{CLERK_ROOT}/v1/client/sign_ins"

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

    credentials["identifier"] = credentials["email"]
    credentials.pop("email")

    session = requests.Session()
    cookie_jar_file = http.cookiejar.MozillaCookieJar(COOKIE_FILENAME)
    session.cookies = cookie_jar_file  # type: ignore
    headers = {
        "Accept-Encoding": "identity",
        "Origin": APP_ROOT,
        "Referer": APP_ROOT,
        "User-Agent": f"finary_uapi {__version__}",
    }
    logging.debug(f"Signing in with {credentials['identifier']}")
    x = session.post(signin_url, data=credentials, headers=headers)
    if x.status_code == 200:
        xjson = x.json()
        if xjson["response"]["status"] == "needs_second_factor":
            if not otp_code:
                raise RuntimeError("OTP code is required and has not been provided")
            logging.debug("Sending OTP code")
            sia = xjson["response"]["id"]
            second_factor_ulr = (
                f"{CLERK_ROOT}/v1/client/sign_ins/{sia}/attempt_second_factor"
            )
            data = {"strategy": "totp", "code": otp_code}
            x = session.post(second_factor_ulr, data=data, headers=headers)
            xjson = x.json()  # replace response

        if errors := xjson.get("errors", None):
            messages = ", ".join([error["long_message"] for error in errors])
            raise RuntimeError(f"Login failed: {messages}")

        if xjson["response"]["status"] == "complete":
            clerk_session = xjson["client"]["sessions"][0]
            session_id = clerk_session["id"]
            session_token = clerk_session["last_active_token"]["jwt"]
            data = {"session_token": session_token, "session_id": session_id}
            with open(JWT_FILENAME, "w") as json_file:
                json.dump(data, json_file)
            cookie_jar_file.save()
            logging.debug("Sign in successful!")

    return x.json()
