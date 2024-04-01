import asyncio
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.contexts.bulk.records import helpers
from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import RecordsUpdate, RecordUpdate
from argilla_server.search_engine import SearchEngine
from argilla_server.validators.records import RecordUpdateValidator


class RecordsUpdateBulk:

    def __init__(self, db: AsyncSession, search_engine: SearchEngine):
        self._db = db
        self._search_engine = search_engine

    async def update_dataset_records(self, dataset: Dataset, records_update: RecordsUpdate) -> None:

        # TODO: This validation should be placed as a pydantic model validation
        #  but the expected message would change. So, we keep it here for now
        record_ids = [r.id for r in records_update.items]
        if len(record_ids) != len(set(record_ids)):
            raise ValueError("Found duplicate records IDs")

        records = []
        async with self._db.begin_nested():
            records_by_id = await helpers.fetch_records_by_ids(self._db, dataset, record_ids)

            not_found_records = [str(record_id) for record_id in record_ids if record_id not in records_by_id]
            if not_found_records:
                raise ValueError(f"Found records that do not exist: {', '.join(not_found_records)}")

            for idx, record_update in enumerate(records_update.items):
                try:
                    record_found = records_by_id[record_update.id]

                    RecordUpdateValidator(record_update).validate_for(dataset)

                    # TODO(@frascuchon): Review this code and improve it
                    if self._metadata_is_set(record_update):
                        record_found.metadata_ = record_update.metadata

                    records.append(record_found)
                except ValueError as ex:
                    raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex

            self._db.add_all(records)
            await self._db.flush(records)

            await self._update_records_relationships(records, records_update)
            await helpers.preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()

    async def _update_records_relationships(self, records: List[Record], records_update: RecordsUpdate) -> None:
        await asyncio.gather(
            helpers.upsert_records_suggestions(self._db, records, records_update.items),
            helpers.upsert_records_vectors(self._db, records, records_update.items),
        )

    def _metadata_is_set(self, record_update: RecordUpdate) -> bool:
        return "metadata_" in record_update.__fields_set__