# Packages
import json
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
    def get_current_time_in_str(fmt: str) -> str:
        """
        Returns current datetime in string format

        Args:
            fmt: time format (%d-%m-%Y)

        Returns:
            str: datetime in string
        """
        return datetime.now().strftime(fmt)

    @staticmethod
    def minute_to_seconds(minute):
        return minute * 60

    @staticmethod
    def convert_to_dict(data: str) -> dict:
        """
        Convert json string data to dict
        Args:
            data: json string
        Returns:
            dict: converted json string into dict
        """
        return json.loads(data)

    @staticmethod
    def convert_to_json(data: dict) -> str:
        """
        Converts dict to json string
        Args:
            data: dict data
        Returns:
            str: converted dict into string
        """
        return json.dumps(data)
