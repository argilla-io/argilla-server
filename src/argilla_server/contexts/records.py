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

from typing import List, Optional, Sequence, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import RecordCreate, RecordUpdate, RecordUpsert
from argilla_server.search_engine import SearchEngine


async def upsert_dataset_records(
    db: AsyncSession,
    search_engine: SearchEngine,
    dataset: Dataset,
    records_upsert: List[RecordUpsert],
) -> List[Record]:

    records = []
    async with db.begin_nested():
        record_ids = [record.id for record in records_upsert]
        found_records = await _list_records_by_ids_and_dataset_id(db, record_ids, dataset.id)

        for record_upsert, record_found in zip(records_upsert, found_records):
            record = await _upsert_record_model(db, dataset, record_found, record_upsert)
            records.append(record)

        await db.flush(records)
        await search_engine.index_records(dataset, records)

    await db.commit()
    return records


async def _list_records_by_ids_and_dataset_id(
    db: "AsyncSession", records_ids: Sequence[UUID], dataset_id: UUID
) -> List[Union[Record, None]]:

    query = select(Record).filter(Record.dataset_id == dataset_id).filter(Record.id.in_(records_ids))

    result = await db.execute(query)
    records = result.unique().scalars().all()

    # Preserve the order of the `record_ids` list
    record_order_map = {record.id: record for record in records}
    ordered_records = [record_order_map.get(record_id, None) for record_id in records_ids]

    return ordered_records


async def _upsert_record_model(
    db: AsyncSession,
    dataset: Dataset,
    found_record: Optional[Record],
    record_upsert: RecordUpsert,
) -> Record:

    if found_record:
        record_update = RecordUpdate(metadata=record_upsert.metadata)
        return await _update_record_model(db, dataset, record=found_record, record_update=record_update)
    else:
        record_create = RecordCreate(
            fields=record_upsert.fields,
            metadata_=record_upsert.metadata,
            external_id=record_upsert.external_id,
        )
        return await _create_record_model(db, dataset, record_create=record_create)


async def _create_record_model(db: AsyncSession, dataset: Dataset, record_create: RecordCreate) -> Record:
    # TODO(@frascuchon): Validate the record_create object
    return await Record.create(
        db,
        fields=record_create.fields,
        metadata_=record_create.metadata,
        external_id=record_create.external_id,
        dataset_id=dataset.id,
        autocommit=False,
    )


async def _update_record_model(
    db: AsyncSession, dataset: Dataset, record: Record, record_update: RecordUpdate
) -> Record:
    # TODO(@frascuchon): Validate the record_update object
    return await record.update(db, metadata_=record_update.metadata_, replace_dict=True, autocommit=False)
