# -*- coding: utf-8 -*-

import os
import hmac
import binascii
import requests
from hashlib import sha1

PTV_BASE_URL = "https://timetableapi.ptv.vic.gov.au"


def _prepare_api_request(url, params=None, user_id=None, api_key=None):
    r"""
    Prepare a request for a call to the Public Transport Victoria API.

    :param url:
        The url to sign (relative to the base URL, e.g., `/v3/routes`)

    :param params: [optional]
        The parameters to supply to the API call.

    :param user_id: [optional]
        The PTV API user ID. If `None` is supplied then this will be retrieved
        from the `PTV_USER_ID` environment variable.

    :param api_key: [optional]
        The PTV API key associated with the `user_id`. If `None` is supplied
        then this will be retrieved from the `PTV_API_KEY` environment variable.
    
    :returns:
        An absolute URL and a dictionary containing any existing params, as well
        as the required user id and signature.
    """

    params = params.copy() if params is not None else {}
    params["devid"] = user_id or os.environ.get("PTV_USER_ID", None)

    url = "/{}".format(url.lstrip(" /"))
    api_key = api_key or os.environ.get("PTV_API_KEY", None)

    hashed = hmac.new(
        api_key, 
        "{}?{}".format(url, requests.PreparedRequest._encode_params(params)),
        sha1)
    params["signature"] = hashed.hexdigest()

    return (PTV_BASE_URL + url, params)


url, params = _prepare_api_request("/v3/routes/")

request = requests.get(url, params=params)


print(request)


