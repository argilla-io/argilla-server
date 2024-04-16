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

from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import StrictStr

from argilla_server.pydantic_v1 import BaseModel, Field, validator
from argilla_server.schemas.v1.records import Record, RecordCreate

RECORDS_BULK_CREATE_MIN_ITEMS = 1
RECORDS_BULK_CREATE_MAX_ITEMS = 500

RECORDS_BULK_UPDATE_MIN_ITEMS = 1
RECORDS_BULK_UPDATE_MAX_ITEMS = 500

RECORDS_BULK_UPSERT_MIN_ITEMS = 1
RECORDS_BULK_UPSERT_MAX_ITEMS = 500


class RecordsBulk(BaseModel):
    items: List[Record]


class RecordsBulkWithUpdateInfo(RecordsBulk):
    updated_item_ids: List[UUID]


class RecordsBulkCreate(BaseModel):
    items: List[RecordCreate] = Field(
        ..., min_items=RECORDS_BULK_CREATE_MIN_ITEMS, max_items=RECORDS_BULK_CREATE_MAX_ITEMS
    )

    @validator("items")
    @classmethod
    def check_unique_external_ids(cls, items: List[RecordCreate]) -> List[RecordCreate]:
        """Check that external_ids are unique"""
        external_ids = [item.external_id for item in items if item.external_id is not None]
        if len(external_ids) != len(set(external_ids)):
            raise ValueError("External IDs must be unique")

        return items


# class RecordUpdate(_RecordUpdate):
#     id: Optional[UUID]
#     external_id: Optional[str]
#
#     @root_validator(skip_on_failure=True)
#     @classmethod
#     def check_id_or_external_id(cls, values: dict) -> dict:
#         """Check that either 'id' or 'external_id' is provided"""
#         record_id = values.get("id")
#         external_id = values.get("external_id")
#
#         if record_id is None and external_id is None:
#             raise ValueError("Either 'id' or 'external_id' must be provided")
#
#         return values
#
#
# class RecordsBulkUpdate(RecordsBulkCreate):
#     items: List[RecordUpdate] = Field(
#         ..., min_items=RECORDS_BULK_UPDATE_MIN_ITEMS, max_items=RECORDS_BULK_UPDATE_MAX_ITEMS
#     )


class RecordUpsert(RecordCreate):
    id: Optional[UUID]
    fields: Optional[Dict[str, Union[StrictStr, None]]]


class RecordsBulkUpsert(RecordsBulkCreate):
    items: List[RecordUpsert] = Field(
        ..., min_items=RECORDS_BULK_UPSERT_MIN_ITEMS, max_items=RECORDS_BULK_UPSERT_MAX_ITEMS
    )
