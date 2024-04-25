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

import asyncio
from datetime import datetime
from typing import List, Union, Dict
from uuid import UUID

import argilla_server.bulk.records_bulk
import argilla_server.contexts.records
from argilla_server.schemas.v1.records_bulk import RecordUpdate, RecordsBulkUpdate, RecordsBulk
from argilla_server.validators.records_bulk import RecordsBulkUpdateValidator
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.models import Dataset, Record
from argilla_server.search_engine import SearchEngine


class UpdateRecordsBulk:

    def __init__(self, db: AsyncSession, search_engine: SearchEngine):
        self._db = db
        self._search_engine = search_engine

    async def update_records_bulk(self, dataset: Dataset, records_update: RecordsBulkUpdate) -> RecordsBulk:
        found_records = await self._fetch_existing_dataset_records(dataset, records_update.items)
        await RecordsBulkUpdateValidator(records_update, db=self._db).validate_for(dataset, found_records)

        async with self._db.begin_nested():
            records = []
            for record_update in records_update.items:
                if self._metadata_is_set(record_update):
                    record_found = found_records[record_update.external_id or record_update.id]

                    record_found.metadata_ = record_update.metadata
                    record_found.updated_at = datetime.utcnow()

                    records.append(record_found)

            self._db.add_all(records)
            await self._db.flush(records)

            await self._update_records_relationships(records, records_update.items)
            await argilla_server.bulk.records_bulk._preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()
        return RecordsBulk(items=records)

    async def _update_records_relationships(
        self,
        records: List[Record],
        records_update: List[RecordUpdate],
    ) -> None:
        records_and_suggestions = list(zip(records, [r.suggestions for r in records_update]))
        records_and_vectors = list(zip(records, [r.vectors for r in records_update]))

        await asyncio.gather(
            argilla_server.bulk.records_bulk._upsert_records_suggestions(self._db, records_and_suggestions),
            argilla_server.bulk.records_bulk._upsert_records_vectors(self._db, records_and_vectors),
        )

    async def _fetch_existing_dataset_records(
        self,
        dataset: Dataset,
        record_update: List[RecordUpdate],
    ) -> Dict[Union[UUID, str], Record]:

        records_by_external_id = await argilla_server.contexts.records.fetch_records_by_external_ids_as_dict(
            self._db, dataset, [r.external_id for r in record_update]
        )
        records = records_by_external_id

        records_by_id = await argilla_server.contexts.records.fetch_records_by_ids_as_dict(
            self._db, dataset, [r.id for r in record_update if r.id not in records_by_external_id]
        )
        records.update(records_by_id)

        return records

    def _metadata_is_set(self, record_update: RecordUpdate) -> bool:
        return "metadata_" in record_update.__fields_set__
