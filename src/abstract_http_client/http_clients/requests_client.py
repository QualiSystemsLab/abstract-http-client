"""
This class can be instantiated directly, or subclassed to change signature / add methods
"""
import logging

from abstract_http_client.http_clients.http_client_base import HttpClientBase
from abstract_http_client.http_services.requests_service import RequestsService


class RequestsClient(HttpClientBase):
    """ Instantiate or Inherit from this class to start writing api client """

    def __init__(
        self,
        host,
        user="",
        password="",
        token="",
        logger: logging.Logger = None,
        port: int = None,
        use_https=True,
        ssl_verify=True,
        proxies: dict = None,
        show_insecure_warning=True,
    ):
        super().__init__(user, password, token, logger)
        self._rest_service = RequestsService(host, port, logger, use_https, ssl_verify, proxies, show_insecure_warning)

    @property
    def rest_service(self) -> RequestsService:
        return self._rest_service
