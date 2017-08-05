# -*- coding: utf-8 -*-

from base import BaseClient

__all__ = ["ClientV2"]

class ClientV2(BaseClient):

    API_VERSION = 2.3


    @property
    def healthcheck(self):
        """
        Return the health status of the remote API.
        """
        return self._request("healthcheck")



    def _lines_by_mode(self, route_type, route_name=None):
        params = dict() if route_name is None else dict(name=route_name)
        return self._request("lines/mode/{}".format(route_type), params)


    def _stops_on_a_line(self, route_type, line_id):
        return self._request("mode/{route_type}/line/{line_id}/stops-for-line"\
            .format(route_type=route_type, line_id=line_id))


    def _specific_next_departures(self, route_type, line_id, stop_id,
        direction_id, limit=5, for_utc=None, include_cancelled=False):

        return self._request(
            "mode/{route_type}/line/{line_id}/stop/{stop_id}/"
            "directionid/{direction_id}/all/limit/{limit}".format(
                route_type=route_type, line_id=line_id, stop_id=stop_id,
                direction_id=direction_id, limit=5))

    def _broad_next_departures(self, route_type, stop_id, limit=5,
        include_cancelled=False):

        return self._request(
            "mode/{route_type}/stop/{stop_id}/departures/by-destination/limit/{limit}"\
            .format(route_type=route_type, stop_id=stop_id, limit=limit))
