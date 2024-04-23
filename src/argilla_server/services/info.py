#  coding=utf-8
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
from typing import Any, Dict, Optional, Union

import psutil
from fastapi import Depends

from argilla_server._version import __version__ as version
from argilla_server.daos.backend import GenericElasticEngineBackend
from argilla_server.pydantic_v1 import BaseModel, BaseSettings, Field
from argilla_server.settings import settings


def size(bytes):
    system = [
        (1024**5, "P"),
        (1024**4, "T"),
        (1024**3, "G"),
        (1024**2, "M"),
        (1024**1, "K"),
        (1024**0, "B"),
    ]

    factor, suffix = None, None
    for factor, suffix in system:
        if bytes >= factor:
            break

    amount = int(bytes / factor)
    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple

    return str(amount) + suffix


class ArgillaInfo(BaseModel):
    show_huggingface_space_persistant_storage_warning: Optional[bool]


class HuggingfaceInfo(BaseSettings):
    space_id: str = Field(None, env="SPACE_ID")
    space_title: str = Field(None, env="SPACE_TITLE")
    space_subdomain: str = Field(None, env="SPACE_SUBDOMAIN")
    space_host: str = Field(None, env="SPACE_HOST")
    space_repo_name: str = Field(None, env="SPACE_REPO_NAME")
    space_author_name: str = Field(None, env="SPACE_AUTHOR_NAME")
    space_persistant_storage_enabled: bool = Field(False, env="PERSISTANT_STORAGE_ENABLED")

    @property
    def is_running_on_huggingface(self) -> bool:
        return bool(self.space_id)


_huggingface_info = HuggingfaceInfo()


class ApiInfo(BaseModel):
    """Basic api info"""

    version: str


class ApiStatus(ApiInfo):
    """The argilla api status model"""

    argilla: ArgillaInfo
    elasticsearch: Dict[str, Any]
    huggingface: Optional[HuggingfaceInfo]
    mem_info: Dict[str, Any]


class ApiInfoService:
    """
    The api info service
    """

    _INSTANCE = None

    @classmethod
    def get_instance(
        cls,
        backend: GenericElasticEngineBackend = Depends(GenericElasticEngineBackend.get_instance),
    ) -> "ApiInfoService":
        """
        Creates an api info service
        """

        if not cls._INSTANCE:
            cls._INSTANCE = ApiInfoService(backend)
        return cls._INSTANCE

    def __init__(self, es: GenericElasticEngineBackend):
        self.__es__ = es

    def api_status(self) -> ApiStatus:
        """Returns the current api status"""
        return ApiStatus(
            version=str(version),
            argilla=self._argilla_info(),
            elasticsearch=self._elasticsearch_info(),
            huggingface=self._huggingface_info(),
            mem_info=self._api_memory_info(),
        )

    def _argilla_info(self) -> ArgillaInfo:
        argilla_info = ArgillaInfo()

        if _huggingface_info.is_running_on_huggingface:
            argilla_info.show_huggingface_space_persistant_storage_warning = (
                settings.show_huggingface_space_persistant_storage_warning
            )

        return argilla_info

    def _elasticsearch_info(self) -> Dict[str, Any]:
        """Returns the elasticsearch cluster info"""
        return self.__es__.client.get_cluster_info()

    def _huggingface_info(self) -> Union[HuggingfaceInfo, None]:
        if _huggingface_info.is_running_on_huggingface:
            return _huggingface_info

    @staticmethod
    def _api_memory_info() -> Dict[str, Any]:
        """Fetch the api process memory usage"""
        process = psutil.Process(os.getpid())
        return {k: size(v) for k, v in process.memory_info()._asdict().items()}
