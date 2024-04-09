import asyncio
from datetime import datetime
from typing import List, Dict, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.bulk import helpers
from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import RecordCreate
from argilla_server.schemas.v1.records_bulk import (
    RecordsBulkCreate,
    RecordsBulk,
    RecordsBulkUpsert,
    RecordsBulkWithUpdateInfo,
    RecordUpsert,
)
from argilla_server.search_engine import SearchEngine
from argilla_server.validators.records_bulk import RecordsBulkCreateValidator, RecordsBulkUpsertValidator


class CreateRecordsBulk:

    def __init__(self, db: AsyncSession, search_engine: SearchEngine):
        self._db = db
        self._search_engine = search_engine

    async def create_records_bulk(self, dataset: Dataset, bulk_create: RecordsBulkCreate) -> RecordsBulk:
        await RecordsBulkCreateValidator(bulk_create, db=self._db).validate_for(dataset)

        async with self._db.begin_nested():
            records = [
                Record(
                    fields=record_create.fields,
                    metadata_=record_create.metadata,
                    external_id=record_create.external_id,
                    dataset_id=dataset.id,
                )
                for record_create in bulk_create.items
            ]

            self._db.add_all(records)
            await self._db.flush(records)

            await self._upsert_records_relationships(records, bulk_create.items)
            await helpers.preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()
        return RecordsBulk(items=records)

    async def _upsert_records_relationships(self, records: List[Record], records_create: List[RecordCreate]) -> None:

        records_and_suggestions = list(zip(records, [r.suggestions for r in records_create]))
        records_and_responses = list(zip(records, [r.responses for r in records_create]))
        records_and_vectors = list(zip(records, [r.vectors for r in records_create]))

        await asyncio.gather(
            helpers.upsert_records_suggestions(self._db, records_and_suggestions),
            helpers.upsert_records_responses(self._db, records_and_responses),
            helpers.upsert_records_vectors(self._db, records_and_vectors),
        )

    def _metadata_is_set(self, record_create: RecordCreate) -> bool:
        return "metadata" in record_create.__fields_set__


class UpsertRecordsBulk(CreateRecordsBulk):

    async def upsert_records_bulk(self, dataset: Dataset, bulk_upsert: RecordsBulkUpsert) -> RecordsBulkWithUpdateInfo:

        found_records = await self._fetch_existing_dataset_records(dataset, bulk_upsert.items)
        # found_records is passed to the validator to avoid querying the database again, but ideally, it should be
        # computed inside the validator
        RecordsBulkUpsertValidator(self._db, bulk_upsert, found_records).validate_for(dataset)

        records = []
        async with self._db.begin_nested():
            for record_upsert in bulk_upsert.items:
                record = found_records.get(record_upsert.external_id or record_upsert.id)
                if not record:
                    records.append(
                        Record(
                            fields=record_upsert.fields,
                            metadata_=record_upsert.metadata,
                            external_id=record_upsert.external_id,
                            dataset_id=dataset.id,
                        )
                    )
                elif self._metadata_is_set(record_upsert):
                    record.metadata_ = record_upsert.metadata
                    record.updated_at = datetime.utcnow()

                    records.append(record)

            self._db.add_all(records)
            await self._db.flush(records)

            await self._upsert_records_relationships(records, bulk_upsert.items)

            await helpers.preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()

        return RecordsBulkWithUpdateInfo(
            items=records,
            updated_item_ids=[record.id for record in found_records.values()],
        )

    async def _fetch_existing_dataset_records(
        self,
        dataset: Dataset,
        records_upsert: List[RecordUpsert],
    ) -> Dict[Union[str, UUID], Record]:

        records_by_external_id = await helpers.fetch_records_by_external_ids(
            self._db, dataset, [r.external_id for r in records_upsert]
        )
        records_by_id = await helpers.fetch_records_by_ids(
            self._db, dataset, [r.id for r in records_upsert if r.id not in records_by_external_id]
        )

        return {**records_by_external_id, **records_by_id}