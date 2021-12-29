[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python/)
[![Lint and Test](https://github.com/QualiSystemsLab/abstract-http-client/actions/workflows/lint-test.yml/badge.svg)](https://github.com/QualiSystemsLab/abstract-http-client/actions/workflows/lint-test.yml)


# Abstract Http Client

This project is a starting template for quickly implementing a python REST api client. A concrete base class encapsulating the popular [requests](https://docs.python-requests.org/en/latest/) library is provided. Abstract base class building blocks for integrating other http libraries (such as aiohttp, etc.) are also available. The main advantage to using this base class as a starting point is to save on common boilerplate actions, which are highlighted below.


### Basic Features
- Setup of session object and common general attributes
- helper methods to send requests with session
- Validation and debug logging of all requests sent
- internal counter of requests sent
- Context manager to manage session tokens (login / logout methods must be implemented)
- Composable client and service classes

### Installation
```
pip install abstract-http-client
```

### Basic Usage

- Sample implementation of api client that has no auth

```python
from abstract_http_client.http_clients.requests_client import RequestsClient
import json

class JsonPlaceholderApiClient(RequestsClient):
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
  print(json.dumps(users[:2], indent=4))
  print(f"total requests sent {api.rest_service.request_counter}")

```
### Auth Client Sample
- Example that requires login and authorization header on every request
- Implement a login method - here it stores header on session object
- Base Class context managers call Logout on __exit__ by default
- Login not in __enter__ by default, can be added if prefer to have context manager trigger login. Or just put into __init__

```python
from abstract_http_client.http_clients.requests_client import RequestsClient


class SampleAuthClient(RequestsClient):
  def __init__(self, host, user, password):
    super().__init__(host=host, user=user, password=password)
    self.login()

  def login(self):
    """  sample login - getting token and storing on requests session object """
    data = {"user": self.user, "password": self.password}
    self.token = self.rest_service.request_put(uri="/login", json=data)
    self.rest_service.session.headers.update({"Authorization": self.token})

  def logout(self):
    """  sample logout - invalidating token and clearing session auth header """
    self.rest_service.request_delete(uri=f"/logout/{self.token}")
    self.rest_service.session.headers.pop({"Authorization": self.token})

  def get_stuff(self) -> dict:
    """ NOTE: this is pseudocode, not real endpoint """
    return self.rest_service.request_get("/stuff").json()


if __name__ == "__main__":
  # Context manager will handle api logout
  with SampleAuthClient(host="192.168.1.3", user="admin", password="admin") as api:
    
    # call your api here 
    stuff = api.get_stuff()
    # Do more stuff
```
