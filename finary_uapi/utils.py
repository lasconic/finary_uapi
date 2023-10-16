import json
import logging
import requests
from .constants import CREDENTIAL_FILE, GOOGLE_MAP_API_ROOT

cred_file = open(CREDENTIAL_FILE, "r")
credentials = json.load(cred_file)
GOOGLE_API_KEY = credentials["google_api"]

def get_and_print(session: requests.Session, url: str):
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()

# Get place_id from Google Map API from address (can be more precise with gps coordinate by using format <address>&circle:<radius-in-meter>@<lat>,<lng>)
# If multiple candidates, will return only the first one
def get_real_estate_placeid ( search_str: str):
    GMAP_Req_url = f"{GOOGLE_MAP_API_ROOT}%22{search_str}%22&key={GOOGLE_API_KEY}"
    GMAP_Req = requests.get(GMAP_Req_url)
    data = GMAP_Req.json()
    return data['candidates'][0]['place_id']