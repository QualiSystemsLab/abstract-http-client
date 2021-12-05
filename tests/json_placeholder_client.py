from abstract_http_client.http_clients.requests_client import RequestsClient


class JsonPlaceholderApiClient(RequestsClient):
    def __init__(self, host):
        super().__init__(host=host, use_https=True)

    def get_posts(self):
        return self.rest_service.request_get("/posts").json()

    def add_post(self):
        return self.rest_service.request_post("/posts", json={"post": "my_post"}).json()

    def edit_post(self):
        return self.rest_service.request_put("/posts/1")

    def delete_post(self):
        return self.rest_service.request_delete("/posts/1")
