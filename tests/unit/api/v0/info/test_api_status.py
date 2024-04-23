#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from unittest import mock

import pytest
from argilla_server.services import info
from argilla_server.services.info import HuggingfaceInfo
from argilla_server.settings import settings
from httpx import AsyncClient


@pytest.mark.asyncio
class TestApiStatus:
    def url(self) -> str:
        return "/api/_status"

    async def test_api_status_with_argilla_info(self, async_client: AsyncClient):
        response = await async_client.get(self.url())

        assert response.status_code == 200
        assert response.json()["argilla"] == {
            "show_huggingface_space_persistant_store_warning": True,
        }

    async def test_api_status_with_argilla_info_and_show_huggingface_space_persistant_store_warning_disabled(
        self, async_client: AsyncClient
    ):
        with mock.patch.object(settings, "show_huggingface_space_persistant_store_warning", False):
            response = await async_client.get(self.url())

            assert response.status_code == 200
            assert response.json()["argilla"] == {
                "show_huggingface_space_persistant_store_warning": False,
            }

    async def test_api_status_with_huggingface_info(self, async_client: AsyncClient):
        huggingface_os_environ = {
            "SPACE_ID": "space-id",
            "SPACE_TITLE": "space-title",
            "SPACE_SUBDOMAIN": "space-subdomain",
            "SPACE_HOST": "space-host",
            "SPACE_REPO_NAME": "space-repo-name",
            "SPACE_AUTHOR_NAME": "space-author-name",
            "PERSISTANT_STORAGE_ENABLED": "true",
        }

        with mock.patch.dict(os.environ, huggingface_os_environ):
            with mock.patch.object(info, "_huggingface_info", HuggingfaceInfo()):
                response = await async_client.get(self.url())

                assert response.status_code == 200
                assert response.json()["huggingface"] == {
                    "space_id": "space-id",
                    "space_title": "space-title",
                    "space_subdomain": "space-subdomain",
                    "space_host": "space-host",
                    "space_repo_name": "space-repo-name",
                    "space_author_name": "space-author-name",
                    "space_persistant_storage_enabled": True,
                }

    async def test_api_status_with_no_huggingface_info(self, async_client: AsyncClient):
        response = await async_client.get(self.url())

        assert response.status_code == 200
        assert "huggingface" not in response.json()
