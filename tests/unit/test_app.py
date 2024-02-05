from typing import cast

from starlette.routing import Mount
from starlette.testclient import TestClient

from argilla_server.settings import settings
from argilla_server._app import create_server_app


class TestApp:
    def test_create_app_with_base_url(self, owner_auth_header: dict):
        settings.base_url = "/new/base/url"
        app = create_server_app()

        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 404

        response = client.get("/new/base/url")
        assert response.status_code == 200

        response = client.get("/api/_info")
        assert response.status_code == 404

        response = client.get("/new/base/url/api/_info")
        assert response.status_code == 200

        assert len(app.routes) == 1
        assert cast(Mount, app.routes[0]).path == "/new/base/url"
