import os

import requests
from dotenv import load_dotenv


def get_records():
    """
    Retrieve all REDCap records and return them as Python objects.
    """
    load_dotenv()

    redcap_url = os.getenv("REDCAP_API_URL")
    api_token = os.getenv("REDCAP_API_TOKEN")

    if redcap_url is None or api_token is None:
        raise ValueError(
            "Missing REDCAP_API_URL or REDCAP_API_TOKEN in .env"
        )

    payload = {
        "token": api_token,
        "content": "record",
        "format": "json",
        "returnFormat": "json",
    }

    response = requests.post(redcap_url, data=payload)
    response.raise_for_status()

    return response.json()