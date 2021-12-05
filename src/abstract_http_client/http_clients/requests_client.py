"""
Abstract Base Class for rest api implementations (don't instantiate directly)
"""
import logging

from abstract_http_client.http_clients.http_client_base import HttpClientBase
from abstract_http_client.http_services.requests_service import RequestsService


class AbstractRequestsClient(HttpClientBase):
    """ Inherit from this class to start writing api client """

    def __init__(
        self,
        host,
        user="",
        password="",
        token="",
        logger: logging.Logger = None,
        port: int = None,
        use_https=False,
        ssl_verify=False,
        proxies: dict = None,
    ):
        super().__init__(user, password, token, logger)
        self._rest_service = RequestsService(host, port, logger, use_https, ssl_verify, proxies)

    @property
    def rest_service(self) -> RequestsService:
        return self._rest_service
