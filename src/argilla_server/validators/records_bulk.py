from typing import Dict, List, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.bulk import helpers
from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import RecordCreate
from argilla_server.schemas.v1.records_bulk import RecordsBulkCreate, RecordsBulkUpsert, RecordUpsert
from argilla_server.validators.records import RecordCreateValidator, RecordUpdateValidator


class RecordsBulkCreateValidator:
    def __init__(self, records_create: RecordsBulkCreate, db: AsyncSession):
        self._records_create = records_create
        self._db = db

    async def validate_for(self, dataset: Dataset) -> None:
        self._validate_dataset_is_ready(dataset)
        await self._validate_external_ids_are_not_present_in_db(dataset)
        self._validate_all_bulk_records(dataset, self._records_create.items)

    def _validate_dataset_is_ready(self, dataset: Dataset) -> None:
        if not dataset.is_ready:
            raise ValueError("records cannot be created for a non published dataset")

    async def _validate_external_ids_are_not_present_in_db(self, dataset: Dataset):
        external_ids = [r.external_id for r in self._records_create.items if r.external_id is not None]
        records_by_external_id = await helpers.fetch_records_by_external_ids(self._db, dataset, external_ids)

        found_records = [str(external_id) for external_id in external_ids if external_id in records_by_external_id]
        if found_records:
            raise ValueError(f"found records with same external ids: {', '.join(found_records)}")

    def _validate_all_bulk_records(self, dataset: Dataset, records_create: List[RecordCreate]):
        for idx, record_create in enumerate(records_create):
            try:
                RecordCreateValidator(record_create).validate_for(dataset)
            except ValueError as ex:
                raise ValueError(f"record at position {idx} is not valid because {ex}") from ex


class RecordsBulkUpsertValidator:
    def __init__(
        self,
        db: AsyncSession,
        records_upsert: RecordsBulkUpsert,
        existing_records_by_external_id_or_record_id: Dict[Union[str, UUID], Record],
    ):
        self._db = db
        self._records_upsert = records_upsert
        self._existing_records_by_external_id_or_record_id = existing_records_by_external_id_or_record_id

    def validate_for(self, dataset: Dataset) -> None:
        self.validate_dataset_is_ready(dataset)
        self._validate_all_bulk_records(dataset, self._records_upsert.items)

    def validate_dataset_is_ready(self, dataset: Dataset) -> None:
        if not dataset.is_ready:
            raise ValueError("records cannot upserted for a non published dataset")

    def _validate_all_bulk_records(self, dataset: Dataset, records_upsert: List[RecordUpsert]):
        for idx, record_upsert in enumerate(records_upsert):
            try:
                record = self._existing_records_by_external_id_or_record_id.get(record_upsert.external_id or record_upsert.id)
                if record:
                    RecordUpdateValidator(record_upsert).validate_for(dataset)
                else:
                    RecordCreateValidator(record_upsert).validate_for(dataset)
            except ValueError as ex:
                raise ValueError(f"record at position {idx} is not valid because {ex}") from ex


# class RecordsBulkUpdateValidator:
#     def __init__(self, records_update: RecordsBulkUpdate, db: AsyncSession):
#         self._records_update = records_update
#         self._db = db
#
#     async def validate_for(self, dataset: Dataset, found_records: Dict[Union[str, UUID], Record]) -> None:
#         self.validate_dataset_is_ready(dataset)
#         await self._validate_record_ids_are_not_present_in_db(dataset)
#
#         for idx, record_update in enumerate(self._records_update.items):
#             try:
#                 if record_update.external_id is not None:
#                     key = record_update.external_id
#                 else:
#                     key = record_update.id
#                 record = found_records.get(key)
#                 if record is None:
#                     raise ValueError(f"Record not found for {key}")
#
#                 RecordUpdateValidator(record_update).validate_for(dataset)
#             except ValueError as ex:
#                 raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex
#
#     async def _validate_record_ids_are_not_present_in_db(self, dataset):
#         record_ids = [r.id for r in self._records_update.items if r.id is not None]
#         if len(record_ids) != len(set(record_ids)):
#             raise ValueError("Found duplicate records IDs")
#
#         records_by_id = await records.fetch_records_by_ids(self._db, dataset, record_ids)
#         not_found_records = [str(record_id) for record_id in record_ids if record_id not in records_by_id]
#
#         if not_found_records:
#             raise ValueError(f"Found records that do not exist: {', '.join(not_found_records)}")
#
#     def validate_dataset_is_ready(self, dataset: Dataset) -> None:
#         if not dataset.is_ready:
#             raise ValueError("Records cannot be updated for a non published dataset")
