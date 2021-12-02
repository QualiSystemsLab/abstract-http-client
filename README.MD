[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python/)

# Abstract Requests Client
This project is a starting template for a REST api wrapper class, encapsulating the popular [requests](https://docs.python-requests.org/en/latest/) libary.
The motivation for this project was to have a re-usable base class when integrating a REST api without an existing python implementation.

This project is an abstract base building block to inherit from and build on top of.

Usage examples can be found below and in tests folder.


### Installation
```
pip install abstract-requests-client
```
## Sample Usage

- Sample implementation of building api client from base class
```python
from abstract_requests_client.abstract_client import AbstractRequestsClient


class JsonPlaceholderApiClient(AbstractRequestsClient):
    def __init__(self, host):
        super().__init__(host=host, use_https=True)

    def get_users(self):
        return self.rest_service.request_get(uri="/users").json()

    def get_posts(self):
        return self.rest_service.request_get("/posts").json()

    def add_post(self):
        return self.rest_service.request_post("/posts", data={"post": "my_post"})

with JsonPlaceholderApiClient(host="jsonplaceholder.typicode.com") as api:
    users = api.get_users()
    print(users)
    print(f"total requests sent {api.rest_service.request_counter}")
    
```

## Usage Notes
- Requests logic is encapsulated into requests_service and added to abstract client by composition
- you can access the requests session directly from the requests service if needed
- All methods run the requests, perform validation on response, then return the Response object. 
  - It's up to your use case what to do with response (response.json(), response.text, etc.)
- Abstract class optionally expects to implement login and logout methods, which are called in context manager methods.


