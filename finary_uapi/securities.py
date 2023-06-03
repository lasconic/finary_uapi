import json
import logging
import requests
from .constants import API_ROOT
from fuzzywuzzy import fuzz


def get_securities(session: requests.Session, query):
    url = f"{API_ROOT}/securities/autocomplete"
    params = {}
    if query:
        params["query"] = query

    x = session.get(url, params=params)
    if x.status_code in (200, 304):
        logging.debug(json.dumps(x.json(), indent=4))
        result = x.json()
    else:
        logging.warning(
            f"Error searching for [{query}]. Status code = [{x.status_code}]"
        )
        result = {"result": []}
    return result


def guess_security(session: requests.Session, security):
    ratio_cut = 45
    result = get_securities(session, security["isin_code"])
    finary_security = {}
    if len(result["result"]) == 0:
        logging.info(
            f"#### Cannot find [{security['isin_code']}] : [{security['description']}]  --- no result"
        )
    elif len(result["result"]) == 1:
        # probably ok, check description
        if security["description"]:
            partial_ratio = fuzz.partial_ratio(
                security["description"].lower(),
                f'{result["result"][0]["symbol"].lower()} {result["result"][0]["name"].lower()}',
            )
        else:
            partial_ratio = (
                100  # no description but one result only, consider it found.
            )
        if partial_ratio > ratio_cut:
            logging.info(
                f"!!! FOUND [{security['isin_code']}] : [{security['description']}] / [{result['result'][0]['name']}]  --- {partial_ratio}%"  # noqa
            )
            finary_security = result["result"][0]
        else:
            logging.info(
                f"###### Cannot find [{security['isin_code']}] : [{security['description']}] / [{result['result'][0]['name']}]  --- ratio too low {partial_ratio}%"  # noqa
            )
    elif result["result"][0]["symbol"] == security["isin_code"]:
        logging.info(
            f"!!!!! FOUND [{security['isin_code']}] : [{security['description']}] / [{result['result'][0]['name']}]"
        )
        finary_security = result["result"][0]
    else:
        candidate_finary_security = {}
        for r in result["result"]:
            if security["currency"] == r["currency"]["code"]:
                candidate_finary_security = r
                break
        if candidate_finary_security:
            if security["description"]:
                partial_ratio = fuzz.partial_ratio(
                    security["description"].lower(),
                    f'{candidate_finary_security["symbol"].lower()} {candidate_finary_security["name"].lower()}',
                )
            else:
                partial_ratio = 100  # match the code and the currency, no description, consider it found.

            if partial_ratio > ratio_cut:
                logging.info(
                    f"!!! FOUND [{security['isin_code']}] : [{security['description']}] / [{candidate_finary_security['name']}]  --- {partial_ratio}% {security['currency']}"  # noqa
                )
                finary_security = candidate_finary_security
            else:
                logging.info(
                    f"###### Cannot find [{security['isin_code']}] : [{security['description']}] / [{candidate_finary_security['name']}]  --- ratio too low {partial_ratio}% despite matching currency"  # noqa
                )
        else:
            logging.info(
                f"######## Cannot find [{security['isin_code']}] : [{security['description']}]  --- more than 1 and isin_code nor currency doesn't match"  # noqa
            )
    logging.debug(json.dumps(result, indent=4))
    return finary_security
