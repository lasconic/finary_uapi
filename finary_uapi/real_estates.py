import json
import logging
import requests
from .constants import API_ROOT

<<<<<<< HEAD
=======

>>>>>>> 3ee0bc30054f24e341e29efcc25587621380d660
def get_real_estates_placeid(session: requests.Session, search_str: str):
    Finary_Req_url = f"{API_ROOT}/real_estates/autocomplete?query={search_str}"
    x = session.get(Finary_Req_url)
    logging.debug(json.dumps(x.json(), indent=4))
    data = x.json()

<<<<<<< HEAD
    return data['result'][0]['place_id']
=======
    return data["result"][0]["place_id"]
>>>>>>> 3ee0bc30054f24e341e29efcc25587621380d660
