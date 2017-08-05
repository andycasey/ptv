# -*- coding: utf-8 -*-

import requests
from hashlib import sha1
from hmac import new as new_hmac
from os import environ

__all__ = ["BaseClient"]

class BaseClient(object):

    API_URL = "https://timetableapi.ptv.vic.gov.au/"

    def __init__(self, user_id=None, api_key=None, **kwargs):
        """
        Initialise a client to interact with the Public Transport Victoria API.

        :param user_id: [optional]
            The PTV API user ID. If `None` is supplied then this will be 
            retrieved from the `PTV_USER_ID` environment variable.

        :param api_key: [optional]
            The PTV API key associated with the `user_id`. If `None` is supplied
            then this will be retrieved from the `PTV_API_KEY` environment 
            variable.
        """

        self._user_id = user_id or environ.get("PTV_USER_ID")
        self._api_key = api_key or environ.get("PTV_API_KEY")
        return None


    def _prepare_request(self, url, params=None):
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

        url = "/v{:.0f}/{}".format(self.API_VERSION, url.lstrip(" /"))

        params = params.copy() if params is not None else {}
        params["devid"] = self._user_id 
        hashed = new_hmac(
            self._api_key, 
            "{}?{}".format(url, requests.PreparedRequest._encode_params(params)),
            sha1)
        params["signature"] = hashed.hexdigest()
        return (self.API_URL + url, params)


    def _request(self, url, params=None, full_output=False, **kwargs):
        r"""
        Execute a request to the Public Transport Victoria API.

        :param url:
            URL for the request.

        :param params: [optional]
            Dictionary to be sent in the query string.

        :param full_output: [optional]
            Return a three-length tuple containing: the API output, the status,
            and the request object. Otherwise, only return the API output.
        """

        url, params = self._prepare_request(url, params=params)
        r = requests.get(url, params=params, **kwargs)
        if not r.ok:
            r.raise_for_status()

        content = r.json()
        try:
            status = content.pop("status")

        except (TypeError, KeyError):
            status = None

        return (content, status, r) if full_output else content
