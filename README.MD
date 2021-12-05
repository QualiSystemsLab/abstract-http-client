[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python/)
[![pre-commit-ci](https://github.com/QualiSystemsLab/abstract-requests-client/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/QualiSystemsLab/abstract-requests-client/actions/workflows/pre-commit.yml)

# Abstract Requests Client

This project is a starting template for a REST api wrapper class, encapsulating the
popular [requests](https://docs.python-requests.org/en/latest/) libary. The motivation for this project was to have a
re-usable base class when integrating a REST api without an existing python implementation.

This project is an abstract base building block to inherit from and build on top of.

Usage examples can be found below and in tests folder.

### Installation

```
pip install abstract-requests-client
```

### Basic Usage

- Sample implementation of api client that has no auth

```python
from abstract_http_client.http_clients.requests_client import AbstractRequestsClient


class JsonPlaceholderApiClient(AbstractRequestsClient):
  def __init__(self, host):
    super().__init__(host=host, use_https=True)

  def get_users(self):
    return self.rest_service.request_get(uri="/users").json()

  def get_posts(self):
    return self.rest_service.request_get("/posts").json()

  def add_post(self):
    return self.rest_service.request_post("/posts", data={"post": "my_post"})


if __name__ == "__main__":
  api = JsonPlaceholderApiClient(host="jsonplaceholder.typicode.com")
  users = api.get_users()
  print(users)
  print(f"total requests sent {api.rest_service.request_counter}")

```
### Auth Client Sample
- Example that requires login and authorization header on every request
- Implement a login method - here it stores header on session object
- Base Class context managers call Logout on __exit__ by default
- Login not in __enter__ by default, can be added if prefer to have context manager trigger login. Or just put into __init__

```python
from abstract_http_client.http_clients.requests_client import AbstractRequestsClient


class SampleAuthClient(AbstractRequestsClient):
  def __init__(self, host, user, password):
    super().__init__(host=host, username=user, password=password)
    self.login()

  def login(self):
    """  sample login - getting token and storing on requests session object """
    data = {"user": self._username, "password": self._password}
    self._token = self.rest_service.request_put(uri="/login")
    self.rest_service.session.headers.update({"Authorization": self._token})

  def logout(self):
    """  sample logout - invalidationg token and clearing session auth header """
    self.rest_service.request_delete(uri=f"/logout/{self._token}")
    self.rest_service.session.headers.pop({"Authorization": self._token})

  def get_stuff(self) -> dict:
    return self.rest_service.request_get("/stuff").json()


if __name__ == "__main__":
  # Context manager will handle api logout
  with SampleAuthClient(host="192.168.1.3", user="admin", password="admin") as api:
    stuff = api.get_stuff()
    # Do more stuff
```

### Base Class Parameters
- The full base init ships with a lot more optional parameters, as seen in the base class
- Extensions define their own signature and pass only what is needed to super call of base

```python
import logging
from abc import ABC, abstractmethod

from abstract_http_client.http_services.requests_service import RequestService


class AbstractRequestsClient(ABC):
  """ Inherit from this class to start writing your generic api """

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
```

## Additional Notes

- Requests logic is encapsulated into requests_service and added to abstract client by composition
- you can access the requests session directly from the requests service if needed
- All methods run the requests, perform validation on response, then return the Response object.
    - It's up to your use case what to do with response (response.json(), response.text, etc.)
- Abstract class optionally expects to implement login and logout methods.


