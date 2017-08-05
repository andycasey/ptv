# -*- coding: utf-8 -*-

import os
import hmac
import binascii
import requests
from hashlib import sha1

PTV_BASE_URL = "https://timetableapi.ptv.vic.gov.au"


def _prepare_api_request(url, params=None, user_id=None, api_key=None, **kwargs):
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


def api_request(url, params=None, full_output=False, request_kwargs=None,
    **kwargs):
    """
    Execute a request to the Public Transport Victoria API.

    :param url:
        URL for the request.

    :param params: [optional]
        Dictionary to be sent in the query string.

    :param full_output: [optional]
        Return a two-length tuple containing the API output and the status.
        Otherwise, only return the API output.
    """

    request_kwargs = request_kwargs or {}
    operation = url.split("/")[2]
    url, params = _prepare_api_request(url, params=params, **kwargs)
    r = requests.get(url, params=params, **request_kwargs)

    if r.ok:
        content = r.json()
        status = content.pop("status")
        
        key = operation if len(content) > 1 else content.keys()[0]

        return (content, status, r) if full_output else content[key]

    else:
        r.raise_for_status()


def route_types(**kwargs):
    """ Return a list of route types and their descriptions. """
    return api_request("/v3/route_types", **kwargs)


def routes(route_name=None, route_types=None, **kwargs):
    """
    Return route names and numbers for all routes of all route types.

    :param route_name: [optional]
        Filter by name of route (accepts partial route name matches).

    :param route_types: [optional]
        Filter by `route_type`. Accepts either an integer or list-like of
        integer values. See :func:`route_types` for descriptions of route types.
    """

    params = dict()
    if route_types is not None:
        if not isinstance(route_types, int):
            # Must be a list-like.
            params["route_types"] \
                = "\n".join(["{:.0f}".format(rt) for rt in route_types])
        else:
            params["route_types"] = "{:.0f}".format(route_types)

    if route_name is not None:
        params["route_name"] = route_name

    return api_request("/v3/routes", params, **kwargs)


def route(route_id, **kwargs):
    """
    Return the route name and number for the specified route ID.
    """
    return api_request("/v3/routes/{0}".format(route_id), **kwargs)



def directions():
    raise NotImplementedError

def disruptions():
    raise NotImplementedError

def patterns(run_id, route_type, **kwargs):
    return api_request("/v3/pattern/run/{run_id}/route_type/{route_type}"\
        .format(run_id=run_id, route_type=route_type), **kwargs)


def search():
    raise NotImplementedError

def runs(route_id, **kwargs):
    """
    Return all trip/service run details for the specified route ID.

    :param route_id:
        The identifer of the route.
    """
    return api_request("/v3/runs/route/{0}".format(route_id), **kwargs)


def departures(stop_id, route_type, route_id=None, **kwargs):
    kwds = dict(stop_id=stop_id, route_type=route_type, route_id=route_id)
    if route_id is None:
        url = "/v3/departures/route_type/{route_type}/stop/{stop_id}"
    else:
        url = "/v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}"

    return api_request(url.format(**kwds), **kwargs)


def runs_by_run_id(run_id, route_type=None, **kwargs):
    raise NotSureYouEverWantThis
    if route_type is None:
        return api_request("/v3/runs/{0}".format(run_id), **kwargs)
    else:
        return api_request("/v3/runs/{run_id}/route_type/{route_type}".format(
            run_id=run_id, route_type=route_type), **kwargs)


def stops(route_id, route_type=None, **kwargs):
    """
    Return all stops on the specified route.

    :param route_id:
        The identifier of the route.

    :param route_type: [optional]
        A number identifying the transport mode. If `None` is given, the stops
        for the first mode of transport available for this route will be 
        returned.
    """

    if route_type is None:
        route_type = route(route_id, **kwargs)["route_type"]

    return api_request("/v3/stops/route/{route_id}/route_type/{route_type}"\
        .format(route_id=route_id, route_type=route_type), **kwargs)



from v3 import V3Client

client = V3Client()

raise a

bus_route = routes(route_name=246)[0]

bus_stops = stops(bus_route["route_id"])


raise a

my_bus_route = routes(route_name=630)[0]

bus_stops = stops(my_bus_route["route_id"])


bus_stop = bus_stops[0]

# Get next departures.
next_departures = departures(
    bus_stop["stop_id"], my_bus_route["route_type"])

for departure in next_departures:
    if departure["estimated_departure_utc"] is not None:
        raise a
    
