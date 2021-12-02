"""
Test api against JSON placeholder mock online api
"""
import pytest
from common import *
from constants import *
from json_placeholder_client import JsonPlaceholderApiClient


def test_post(api_client):
    response = api_client.add_post().json()
    assert isinstance(response, dict)
    pretty_print_response(response)


def test_get_posts(api_client):
    response = api_client.get_posts()
    assert isinstance(response, list)
    print(f"posts count: {len(response)}")


def test_edit_post(api_client):
    response = api_client.edit_post().json()
    assert isinstance(response, dict)
    pretty_print_response(response)


def test_delete_post(api_client):
    response = api_client.delete_post().json()
    assert isinstance(response, dict)
    pretty_print_response(response)