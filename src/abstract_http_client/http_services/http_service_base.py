"""
Generic implementation of working with Requests session object to make requests and validate responses
"""
import logging
from abc import ABC, abstractmethod
from typing import List

import urllib3


def _disable_errors(exception_types: List[urllib3.exceptions.HTTPWarning]):
    for exc_type in exception_types:
        urllib3.disable_warnings(exc_type)


class HttpServiceBase(ABC):
    def __init__(
        self,
        host: str,
        port: int = None,
        logger: logging.Logger = None,
        use_https=False,
        disabled_http_warnings: List[urllib3.exceptions.HTTPWarning] = None,
    ):
        """ Session object passed should be instantiated outside then passed in """
        self._host = host
        self._port = port
        self._use_https = use_https
        self._request_counter = 0
        self._logger = logger
        _disable_errors(disabled_http_warnings)

    @property
    def request_counter(self) -> int:
        return self._request_counter

    def _increment_request_counter(self):
        """ Track request count during session  """
        self._request_counter += 1

    def _build_url(self, uri: str):
        """
        Support passing FULL url or just URI.
        Example - http://{hostname}:{port}/{uri}
        Also allows passing URI as "/endpoint" OR "endpoint"
        """
        if self._host in uri and uri.startswith("http"):
            return uri

        # support passing uri with or without "/"
        if not uri.startswith("/"):
            uri = "/" + uri

        protocol = "https" if self._use_https else "http"
        url = f"{protocol}://{self._host}"
        if self._port:
            url += f":{self._port}"
        url += uri
        return url

    def _debug_log(self, message: str):
        """ Add debug level logging if passed a logger """
        if self._logger:
            self._logger.debug(message)

    @staticmethod
    @abstractmethod
    def _validate_response(response):
        """
        Receive the response, check for http errors and raise exception

        call after making request inside _send_request
        """
        pass
