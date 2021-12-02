import time

import pytest
from constants import *
from json_placeholder_client import JsonPlaceholderApiClient


@pytest.fixture(scope="session")
def api_client() -> JsonPlaceholderApiClient:
    api = JsonPlaceholderApiClient(host=JSON_PLACEHOLDER_API_HOST)
    with api:
        yield api
        print("ending api session")
