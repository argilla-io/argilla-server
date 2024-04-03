import asyncio
from datetime import datetime
from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.contexts.bulk.records import helpers
from argilla_server.models import Record, Dataset
from argilla_server.schemas.v1.records import RecordsUpsert, RecordUpsert
from argilla_server.search_engine import SearchEngine
from argilla_server.validators.records import RecordUpsertValidator


class RecordsUpsertBulk:

    def __init__(self, db: AsyncSession, search_engine: SearchEngine):
        self._db = db
        self._search_engine = search_engine

    async def upsert_dataset_records(self, dataset: Dataset, records_upsert: RecordsUpsert) -> List[Record]:
        helpers.check_dataset_is_ready(dataset)

        records = []
        async with self._db.begin_nested():
            found_records = await self._fetch_existing_dataset_records(dataset, records_upsert.items)
            for idx, (record_upsert, record_found) in enumerate(zip(records_upsert.items, found_records)):
                try:
                    validator = RecordUpsertValidator(record_upsert)
                    if record_found:
                        validator.validate_for(record_found)
                        record = record_found
                        if self._metadata_is_set(record_upsert):
                            record.metadata_ = record_upsert.metadata
                            record_found.updated_at = datetime.utcnow()
                    else:
                        validator.validate_for(dataset)
                        record = Record(
                            fields=record_upsert.fields,
                            metadata_=record_upsert.metadata,
                            external_id=record_upsert.external_id,
                            dataset_id=dataset.id,
                        )
                    records.append(record)
                except ValueError as ex:
                    raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex

            self._db.add_all(records)
            await self._db.flush(records)

            await self._upsert_records_relationships(records, records_upsert)

            await helpers.preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()
        return records

    async def _fetch_existing_dataset_records(
        self,
        dataset: Dataset,
        records_upsert: List[RecordUpsert],
    ) -> List[Union[Record, None]]:

        records_by_external_id = await helpers.fetch_records_by_external_ids(
            self._db, dataset, [r.external_id for r in records_upsert]
        )
        records_by_id = await helpers.fetch_records_by_ids(
            self._db, dataset, [r.id for r in records_upsert if r.id not in records_by_external_id]
        )

        return [
            records_by_external_id.get(record_upsert.external_id) or records_by_id.get(record_upsert.id)
            for record_upsert in records_upsert
        ]

    async def _upsert_records_relationships(self, records: List[Record], records_upsert: RecordsUpsert) -> None:

        records_and_suggestions = list(zip(records, [r.suggestions for r in records_upsert.items]))
        records_and_responses = list(zip(records, [r.responses for r in records_upsert.items]))
        records_and_vectors = list(zip(records, [r.vectors for r in records_upsert.items]))

        await asyncio.gather(
            helpers.upsert_records_suggestions(self._db, records_and_suggestions),
            helpers.upsert_records_responses(self._db, records_and_responses),
            helpers.upsert_records_vectors(self._db, records_and_vectors),
        )

    def _metadata_is_set(self, record_upsert: RecordUpsert) -> bool:
        return "metadata" in record_upsert.__fields_set__
