# Packages
import requests
from datetime import datetime


class Helper:
    @staticmethod
    def request_http_get(url, payload, headers=None, timeout=2) -> requests.Response:
        """
        Http Get requests invocation
        Args:
            url: request url
            payload: payload/parameters passed to the request
            headers: request headers
            timeout: timeout for the request (default=2)
        Returns:
            response object
        """
        return requests.get(url, payload, headers=headers, timeout=timeout)

    @staticmethod
    def get_current_time() -> datetime:
        """
        Returns current datetime object
        """
        return datetime.now()

    @staticmethod
    def minute_to_seconds(minute):
        return minute * 60
