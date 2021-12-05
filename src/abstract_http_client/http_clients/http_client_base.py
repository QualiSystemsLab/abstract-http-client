"""
ABC that defines the context manager behavior and stores base attributes
Not meant to be instantiated
"""
import logging
from abc import ABC


class HttpClientBase(ABC):
    """ store base attributes for login and define context manager methods """

    def __init__(self, user, password, token, logger: logging.Logger):
        self.user = user
        self.password = password
        self.token = token
        self.logger = logger

    def login(self):
        pass

    def logout(self):
        pass

    def __enter__(self):
        """
        Optionally over-ride this to have login occur on context manager
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Trigger logout on leaving context
        """
        self.logout()
