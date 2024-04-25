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
from typing import List

from argilla_server.validators.records import RecordCreateValidator
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.contexts import records as records_ctx
from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import RecordsCreate, RecordCreate
from argilla_server.search_engine import SearchEngine


class CreateRecords:

    def __init__(self, db: AsyncSession, search_engine: SearchEngine):
        self._db = db
        self._search_engine = search_engine

    async def create_records(self, dataset: Dataset, records_create: RecordsCreate) -> List[Record]:
        self._validate_dataset_is_ready(dataset)

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

            await self._create_records_relationships(records, records_create.items)
            await records_ctx.preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()
        return records

    def _validate_dataset_is_ready(self, dataset: Dataset) -> None:
        if not dataset.is_ready:
            raise ValueError("Records cannot be created for a non published dataset")

    async def _create_records_relationships(self, records: List[Record], records_create: List[RecordCreate]) -> None:

        records_and_suggestions = list(zip(records, [r.suggestions for r in records_create]))
        records_and_responses = list(zip(records, [r.responses for r in records_create]))
        records_and_vectors = list(zip(records, [r.vectors for r in records_create]))

        await asyncio.gather(
            records_ctx.upsert_records_suggestions(self._db, records_and_suggestions),
            records_ctx.upsert_records_responses(self._db, records_and_responses),
            records_ctx.upsert_records_vectors(self._db, records_and_vectors),
        )
