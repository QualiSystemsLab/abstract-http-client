[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python/)
[![pre-commit-ci](https://github.com/QualiSystemsLab/abstract-requests-client/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/QualiSystemsLab/abstract-requests-client/actions/workflows/pre-commit.yml)

# Abstract Http Client

This project is a starting template for implementing a REST api client, with a starting template encapsulating the
popular [requests](https://docs.python-requests.org/en/latest/) libary, and the base class building blocks for integrating other http libraries. 
The motivation for this project was to skip boilerplate when working with a REST api that has no existing python implementation.

### Installation
```
pip install abstract-http-client
```

### Basic Usage

- Sample implementation of api client that has no auth

```python
from abstract_http_client.http_clients.requests_client import RequestsClient


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
  print(users)
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
    return self.rest_service.request_get("/stuff").json()


if __name__ == "__main__":
  # Context manager will handle api logout
  with SampleAuthClient(host="192.168.1.3", user="admin", password="admin") as api:
    stuff = api.get_stuff()
    # Do more stuff
```

## Additional Notes
- Requests logic is encapsulated into requests_service and added to abstract client by composition
- you can access the requests session directly from the requests service if needed
- All methods run the requests, perform validation on response, then return the Response object.
    - It's up to your use case what to do with response (response.json(), response.text, etc.)
- Abstract class optionally expects to implement login and logout methods.


