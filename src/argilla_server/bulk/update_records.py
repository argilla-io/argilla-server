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
from typing import List, Union, Tuple

from argilla_server.validators.records import RecordUpdateValidator
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.contexts import records as records_ctx
from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import (
    RecordsUpdate,
    RecordUpdateWithId,
    RecordUpdate,
)
from argilla_server.schemas.v1.suggestions import SuggestionCreate
from argilla_server.search_engine import SearchEngine


class UpdateRecords:

    def __init__(self, db: AsyncSession, search_engine: SearchEngine):
        self._db = db
        self._search_engine = search_engine

    async def update_records(self, dataset: Dataset, records_update: RecordsUpdate) -> None:

        # TODO: This validation should be placed as a pydantic model validation
        #  but the expected message would change. So, we keep it here for now
        record_ids = [r.id for r in records_update.items]
        if len(record_ids) != len(set(record_ids)):
            raise ValueError("Found duplicate records IDs")

        records = []
        async with self._db.begin_nested():
            records_by_id = await records_ctx.fetch_records_by_ids(self._db, dataset, record_ids)

            not_found_records = [str(record_id) for record_id in record_ids if record_id not in records_by_id]
            if not_found_records:
                raise ValueError(f"Found records that do not exist: {', '.join(not_found_records)}")

            for idx, record_update in enumerate(records_update.items):
                try:
                    record_found = records_by_id[record_update.id]

                    RecordUpdateValidator(record_update).validate_for(dataset)

                    if self._metadata_is_set(record_update):
                        record_found.metadata_ = record_update.metadata
                        record_found.updated_at = datetime.utcnow()

                    records.append(record_found)
                except ValueError as ex:
                    raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex

            self._db.add_all(records)
            await self._db.flush(records)

            await self._update_records_relationships(records, records_update.items)

            await records_ctx.preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()

    async def _update_records_relationships(
        self,
        records: List[Record],
        records_update: List[Union[RecordUpdateWithId, RecordUpdate]],
    ) -> None:
        records_and_suggestions = list(zip(records, [r.suggestions for r in records_update]))
        records_and_vectors = list(zip(records, [r.vectors for r in records_update]))

        await asyncio.gather(
            self._update_records_suggestions(records_and_suggestions),
            records_ctx.upsert_records_vectors(self._db, records_and_vectors),
        )

    async def _update_records_suggestions(
        self,
        records_and_suggestions: List[Tuple[Record, List[SuggestionCreate]]],
    ) -> None:

        record_ids = [record.id for record, suggestions in records_and_suggestions if suggestions is not None]

        await records_ctx.delete_suggestions_by_record_ids(self._db, set(record_ids))
        await records_ctx.upsert_records_suggestions(self._db, records_and_suggestions)

    def _metadata_is_set(self, record_update: RecordUpdate) -> bool:
        return "metadata_" in record_update.__fields_set__
