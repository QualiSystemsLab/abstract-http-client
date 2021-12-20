"""
ABC providing some common methods for http service class
Do not instantiate directly
"""
import logging
from abc import ABC, abstractmethod

import urllib3
from urllib3.exceptions import InsecureRequestWarning


def disable_urllib_exception(exc_type: urllib3.exceptions.HTTPWarning):
    urllib3.disable_warnings(exc_type)


def disable_insecure_warning():
    disable_urllib_exception(InsecureRequestWarning)


class HttpServiceBase(ABC):
    def __init__(self, host: str, port: int = None, logger: logging.Logger = None, use_https=True, show_insecure_warning=True):
        self.host = host
        self.port = port
        self._use_https = use_https
        self._request_counter = 0
        self._logger = logger
        if not show_insecure_warning:
            disable_insecure_warning()

    @property
    def request_counter(self) -> int:
        return self._request_counter

    def _increment_request_counter(self):
        """ Track request count during session  """
        self._request_counter += 1

    @abstractmethod
    def _validate_response(self, response):
        """
        Receive the response, check for http errors and raise exception

        call after making request inside _send_request
        """
        pass

    def _build_url(self, uri: str):
        """
        Support passing FULL url or just URI.
        Example - http://{hostname}:{port}/{uri}
        Also allows passing URI as "/endpoint" OR "endpoint"
        """
        if self.host in uri and uri.startswith("http"):
            return uri

        # support passing uri with or without "/"
        if not uri.startswith("/"):
            uri = "/" + uri

        protocol = "https" if self._use_https else "http"
        url = f"{protocol}://{self.host}"
        if self.port:
            url += f":{self.port}"
        url += uri
        return url

    def debug_log(self, message: str):
        """ Add debug level logging if passed a logger """
        if self._logger:
            self._logger.debug(message)

    def exception_log(self, message: str):
        if self._logger:
            self._logger.exception(message)
