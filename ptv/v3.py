# -*- coding: utf-8 -*-

from base import BaseClient

__all__ = ["ClientV3"]

class ClientV3(BaseClient):

    API_VERSION = 3

    @property
    def route_types(self):
        """
        Return a dictionary of route types (as keys) and their descriptions.
        """
        
        content = self._request("route_types")["route_types"]
        return dict([(r["route_type"], r["route_type_name"]) for r in content])



    def departures(self, route_type, stop_id, route_id=None):
        kwds = dict(route_type=route_type, stop_id=stop_id, route_id=route_id)
        if route_id is None:
            url = "departures/route_type/{route_type}/stop/{stop_id}"
        else:
            url = "departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}"

        return self._request(url.format(**kwds))
        