"""
An abstraction on top of the requests library. This class provides the following convenience features
- thin wrapper commands around the 4 main HTTP requests (GET, POST, PUT, DELETE)
- session setup, all requests made by session object
- A request counter attribute tracking the number of requests made per instance session
- debug logging on every step of request build
- validation of each request before return

Recommended to work with session object, but can work on a per request basis as well
"""
import logging
from typing import Tuple, Union

from requests import Request, Response, Session
from requests.models import HTTPBasicAuth, HTTPError

from abstract_http_client.exceptions import *
from abstract_http_client.http_services.constants import HttpVerbs
from abstract_http_client.http_services.http_service_base import HttpServiceBase

auth_type = Union[HTTPBasicAuth, Tuple[str, str]]


class RequestsService(HttpServiceBase):
    def __init__(
        self,
        host: str,
        port: int = None,
        logger: logging.Logger = None,
        use_https=True,
        ssl_verify=True,
        proxies: dict = None,
        insecure_warning=True,
    ):
        super().__init__(host, port, logger, use_https, insecure_warning)
        self._session = Session()
        self._configure_session_settings(proxies, ssl_verify)

    @property
    def session(self) -> Session:
        return self._session

    def _configure_session_settings(self, proxies: dict, ssl_verify: bool):
        if proxies:
            self.debug_log(f"Configuring proxies on session: {proxies}")
            self._session.proxies = proxies
        if ssl_verify:
            self.debug_log(f"Configuring SSL Verify: {proxies}")
            self._session.verify = ssl_verify

    def _validate_response(self, response: Response):
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == 401:
                exc_msg = f"Failed Authentication. {str(e)}"
                self.exception_log(exc_msg)
                raise RestClientUnauthorizedException(exc_msg) from e
            exc_msg = f"Failed Request. {str(e)}"
            self.exception_log(exc_msg)
            raise RestClientException(exc_msg) from e
        return response

    def _send_request(
        self,
        http_verb: str,
        uri: str,
        json: dict = None,
        data: dict = None,
        headers: dict = None,
        params: dict = None,
        files: dict = None,
        cookies: dict = None,
        hooks: dict = None,
        auth: auth_type = None,
    ):
        """
        Central method to build and send request

        - body, headers and file payload conditionally added
        - environment variables merged before sending
        - internal request counter incremented ahead of response validation
        - all steps of request prep logged at debug level
        """
        self.debug_log(f"=== Prepping '{http_verb}' Request ===")
        url = self._build_url(uri)
        self.debug_log(f"Request URL: {url}")
        req = Request(method=http_verb, url=url)

        # add conditional items to request
        if params:
            self.debug_log(f"Adding params: {params}")
            req.params = params

        if headers:
            self.debug_log(f"Adding headers: {headers}")
            req.headers = headers

        if files:
            self.debug_log(f"Adding files payload: {files}")
            req.files = files

        if data:
            self.debug_log(f"Adding passed data: {data}")
            req.data = data

        if json:
            self.debug_log(f"Adding JSON payload: {json}")
            req.json = json

        if auth:
            self.debug_log(f"Adding auth payload: {auth}")
            req.auth = auth

        if cookies:
            self.debug_log(f"Adding cookies: {cookies}")
            req.cookies = cookies

        if hooks:
            self.debug_log(f"Adding hooks: {hooks}")
            req.hooks = hooks

        # Prepare request and merge environment settings into session
        prepped_req = self._session.prepare_request(req)
        settings = self._session.merge_environment_settings(prepped_req.url, {}, None, None, None)
        response = self._session.send(prepped_req, **settings)
        self._increment_request_counter()
        return self._validate_response(response)

    def request_get(
        self,
        uri: str,
        headers: dict = None,
        params: dict = None,
        cookies: dict = None,
        hooks: dict = None,
        auth: auth_type = None,
    ) -> Response:
        return self._send_request(HttpVerbs.GET, uri, headers=headers, params=params, cookies=cookies, hooks=hooks, auth=auth)

    def request_post(
        self,
        uri: str,
        json: dict = None,
        data: dict = None,
        files: dict = None,
        headers: dict = None,
        params: dict = None,
        cookies: dict = None,
        hooks: dict = None,
        auth: auth_type = None,
    ) -> Response:
        """
        Passing 'json' parameter is in line with requests api - https://stackoverflow.com/a/26344315
        Send a file dict example - https://stackoverflow.com/a/22567429
        """
        return self._send_request(HttpVerbs.POST, uri, json, data, headers, params, files, cookies, hooks, auth)

    def request_put(
        self,
        uri: str,
        json: dict = None,
        data: dict = None,
        headers: dict = None,
        params: dict = None,
        cookies: dict = None,
        hooks: dict = None,
        auth: auth_type = None,
    ) -> Response:
        return self._send_request(HttpVerbs.PUT, uri, json, data, headers, params, cookies=cookies, hooks=hooks, auth=auth)

    def request_delete(
        self,
        uri: str,
        headers: dict = None,
        params: dict = None,
        cookies: dict = None,
        hooks: dict = None,
        auth: auth_type = None,
    ) -> Response:
        return self._send_request(
            HttpVerbs.DELETE, uri, headers=headers, params=params, cookies=cookies, hooks=hooks, auth=auth
        )
