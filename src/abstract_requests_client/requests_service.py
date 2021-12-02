"""
Generic implementation of working with Requests session object to make requests and validate responses
"""
import urllib3
import logging

import requests
from requests import Request, Response
from requests.models import HTTPError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RestClientException(Exception):
    pass


class RestClientUnauthorizedException(RestClientException):
    pass


class RequestService:
    def __init__(self, host: str, port: int = None, logger: logging.Logger = None, use_https=False, ssl_verify=False,
                 proxies: dict = None):
        self._host = host
        self._port = port
        self._use_https = use_https
        self._session = requests.Session()
        self._request_counter = 0
        self._logger = logger
        self._configure_session_settings(proxies, ssl_verify)

    @property
    def session(self):
        return self._session

    @property
    def request_counter(self):
        return self._request_counter

    def _configure_session_settings(self, proxies: dict, ssl_verify: bool):
        if proxies:
            self._debug_log(f"Configuring proxies on session: {proxies}")
            self._session.proxies = proxies
        if ssl_verify:
            self._debug_log(f"Configuring SSL Verify: {proxies}")
            self._session.verify = ssl_verify

    def _increment_request_counter(self):
        """ Track request count during session  """
        self._request_counter += 1

    def _build_url(self, uri: str):
        """
        support passing FULL url or just URI.
        Example - http://{hostname}:{port}/{uri}
        Also allows passing URI as "/endpoint" OR "endpoint"
        """
        if self._host in uri and uri.startswith("http"):
            return uri

        # support passing uri with or without "/"
        if not uri.startswith('/'):
            uri = '/' + uri

        protocol = "https" if self._use_https else "http"
        url = f'{protocol}://{self._host}'
        if self._port:
            url += f":{self._port}"
        url += uri
        return url

    @staticmethod
    def _validate_response(response: Response):
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == 401:
                raise RestClientUnauthorizedException(f"Failed Authentication. {str(e)}")
            raise RestClientException(f"Failed Request. {str(e)}")
        return response

    def _debug_log(self, message: str):
        if self._logger:
            self._logger.debug(message)

    def _send_request(self, http_verb: str, uri: str, data: dict = None, headers: dict = None, params: dict = None,
                      files: dict = None):
        """
        Central method to build and send request

        - body, headers and file payload conditionally added
        - environment variables merged before sending
        - internal request counter incremented ahead of response validation
        - all steps of request prep logged at debug level
        """
        self._debug_log(f"=== Prepping '{http_verb}' Request ===")
        url = self._build_url(uri)
        self._debug_log(f"Request URL: {url}")
        req = Request(method=http_verb, url=url)

        if params:
            self._debug_log(f"Adding params: {params}")
            req.params = params

        if headers:
            self._debug_log(f"Adding headers: {headers}")
            req.headers = headers

        if files:
            self._debug_log(f"Adding files payload: {files}")
            req.files = files
            if data:
                self._debug_log(f"Adding data for files request: {data}")

        if data:
            self._debug_log(f"Adding JSON body from data: {data}")
            req.json = data

        # Prepare request and merge environment settings into session
        prepped_req = self._session.prepare_request(req)
        settings = self._session.merge_environment_settings(prepped_req.url, {}, None, None, None)
        response = self._session.send(prepped_req, **settings)
        self._increment_request_counter()
        return self._validate_response(response)

    def request_get(self, uri: str, headers: dict = None, params: dict = None) -> Response:
        return self._send_request("GET", uri, headers=headers, params=params)

    def request_post(self, uri: str, data: dict = None, headers: dict = None, params: dict = None) -> Response:
        return self._send_request("POST", uri, data, headers, params)

    def request_post_files(self, uri: str, data: dict, files: dict, headers: dict = None, params: dict = None) -> Response:
        """
        send files example - https://stackoverflow.com/a/22567429
        """
        return self._send_request("POST", uri, data, headers, params, files)

    def request_put(self, uri: str, data: dict = None, headers: dict = None, params: dict = None) -> Response:
        return self._send_request("PUT", uri, data, headers, params)

    def request_delete(self, uri, headers: dict = None, params: dict = None) -> Response:
        return self._send_request("DELETE", uri, headers=headers, params=params)
