from typing import List, Optional, Union, Dict
from uuid import UUID

from pydantic import StrictStr

from argilla_server.pydantic_v1 import BaseModel, Field, validator
from argilla_server.schemas.v1.records import RecordCreate, Record

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
        ..., min_items=RECORDS_BULK_CREATE_MIN_ITEMS, max_items=RECORDS_BULK_CREATE_MAX_ITEMS
    )
