import asyncio
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.contexts.bulk.records import helpers
from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import RecordsCreate
from argilla_server.search_engine import SearchEngine
from argilla_server.validators.records import RecordCreateValidator


class RecordsCreateBulk:

    def __init__(self, db: AsyncSession, search_engine: SearchEngine):
        self._db = db
        self._search_engine = search_engine

    async def create_dataset_records(
        self,dataset: Dataset, records_create: RecordsCreate
    ) -> List[Record]:
        helpers.check_is_ready_dataset(dataset)

        records = []
        async with self._db.begin_nested():
            for idx, record_create in enumerate(records_create.items):
                try:
                    RecordCreateValidator(record_create).validate_for(dataset)
                    record = Record(
                        fields=record_create.fields,
                        metadata_=record_create.metadata,
                        external_id=record_create.external_id,
                        dataset_id=dataset.id,
                    )
                    records.append(record)
                except ValueError as ex:
                    raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex

            self._db.add_all(records)
            await self._db.flush(records)

            await self._create_records_relationships(records, records_create)
            await helpers.preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()
        return records

    async def _create_records_relationships(
        self, records: List[Record], records_create: RecordsCreate
    ) -> None:

        records_and_suggestions = list(zip(records, [r.suggestions for r in records_create.items]))
        records_and_responses = list(zip(records, [r.responses for r in records_create.items]))
        records_and_vectors = list(zip(records, [r.vectors for r in records_create.items]))

        await asyncio.gather(
            helpers.upsert_records_suggestions(self._db, records_and_suggestions),
            helpers.upsert_records_responses(self._db, records_and_responses),
            helpers.upsert_records_vectors(self._db, records_and_vectors),
        )
