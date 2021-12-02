"""
Abstract Base Class for rest api implementations (don't instantiate directly)
"""
import logging
from abc import ABC, abstractmethod

from abstract_requests_client.requests_service import RequestService


class AbstractRequestsClient(ABC):
    """ Inherit from this class to start writing your api client """

    @abstractmethod
    def __init__(
        self,
        host,
        username="",
        password="",
        token="",
        logger: logging.Logger = None,
        port: int = None,
        use_https=False,
        ssl_verify=False,
        proxies: dict = None,
    ):
        self._rest_service = RequestService(host, port, logger, use_https, ssl_verify, proxies)
        self._logger = logger
        self._username = username
        self._password = password
        self._token = token

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def rest_service(self):
        return self._rest_service

    def login(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def _logout(self):
        try:
            self.logout()
        except NotImplementedError:
            pass

    def __enter__(self):
        """
        This method can be over-ridden for additional functionality
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Do api clean up
        """
        self._logout()
