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

from typing import Dict, Iterable, List, Optional, Sequence, Union
from uuid import UUID

from sqlalchemy import select, sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from argilla_server.models import Dataset, Record, Suggestion
from argilla_server.schemas.v1.records import RecordCreate, RecordUpdate, RecordUpsert
from argilla_server.search_engine import SearchEngine
from argilla_server.validators.records import RecordCreateValidator, RecordUpdateValidator


async def upsert_dataset_records(
    db: AsyncSession,
    search_engine: SearchEngine,
    dataset: Dataset,
    records_upsert: List[RecordUpsert],
) -> List[Record]:

    records = []
    async with db.begin_nested():
        found_records = await _fetch_existing_dataset_records_if_any(db, dataset, records_upsert)

        for record_upsert, record_found in zip(records_upsert, found_records):
            record = await _upsert_record(db, dataset, record_found, record_upsert)
            records.append(record)

        await db.flush(records)
        await search_engine.index_records(dataset, records)

    await db.commit()
    return records


async def _fetch_existing_dataset_records_if_any(
    db: AsyncSession,
    dataset: Dataset,
    records_upsert: List[RecordUpsert],
) -> List[Union[Record, None]]:

    external_ids_map, record_ids_map = {}, {}
    for record_upsert in records_upsert:
        if record_upsert.external_id:
            external_ids_map.setdefault(record_upsert.external_id)
        else:
            record_ids_map.setdefault(record_upsert.id)

    records_by_external_ids = await _list_dataset_records_by_external_ids(db, dataset.id, external_ids_map)
    external_ids_map.update({record.external_id: record for record in records_by_external_ids})

    records_by_ids = await _list_dataset_records_by_ids(db, dataset.id, record_ids_map)
    record_ids_map.update({record.id: record for record in records_by_ids})

    return [
        external_ids_map.get(record_upsert.external_id) or record_ids_map.get(record_upsert.id)
        for record_upsert in records_upsert
    ]


async def _list_dataset_records_by_external_ids(
    db: AsyncSession, dataset_id: UUID, external_ids: Sequence[str]
) -> Sequence[Record]:

    query = select(Record).filter(Record.external_id.in_(external_ids), Record.dataset_id == dataset_id)
    return (await db.execute(query)).unique().scalars().all()


async def _list_dataset_records_by_ids(
    db: AsyncSession, dataset_id: UUID, record_ids: Sequence[UUID]
) -> Sequence[Record]:

    query = select(Record).filter(Record.id.in_(record_ids), Record.dataset_id == dataset_id)
    return (await db.execute(query)).unique().scalars().all()


async def _upsert_record(
    db: AsyncSession,
    dataset: Dataset,
    record: Optional[Record],
    record_upsert: RecordUpsert,
) -> Record:
    if record:
        record_update = RecordUpdate(metadata=record_upsert.metadata)
        return await _update_record(db, dataset, record=record, record_update=record_update)

    record_create = RecordCreate(
        fields=record_upsert.fields, metadata_=record_upsert.metadata, external_id=record_upsert.external_id
    )
    return await _create_record(db, dataset, record_create=record_create)


async def _create_record(db: AsyncSession, dataset: Dataset, record_create: RecordCreate) -> Record:
    RecordCreateValidator(record_create).validate_for(dataset)
    return await Record.create(
        db,
        fields=record_create.fields,
        metadata_=record_create.metadata,
        external_id=record_create.external_id,
        dataset_id=dataset.id,
        autocommit=False,
    )


async def _update_record(db: AsyncSession, dataset: Dataset, record: Record, record_update: RecordUpdate) -> Record:
    RecordUpdateValidator(record_update).validate_for(dataset)
    return await record.update(db, metadata_=record_update.metadata_, replace_dict=True, autocommit=False)


async def list_dataset_records_by_ids(
    db: AsyncSession, dataset_id: UUID, record_ids: Sequence[UUID]
) -> Sequence[Record]:

    query = select(Record).filter(Record.id.in_(record_ids), Record.dataset_id == dataset_id)
    return (await db.execute(query)).unique().scalars().all()


async def list_dataset_records_by_external_ids(
    db: AsyncSession, dataset_id: UUID, external_ids: Sequence[str]
) -> Sequence[Record]:

    query = (
        select(Record)
        .filter(Record.external_id.in_(external_ids), Record.dataset_id == dataset_id)
        .options(selectinload(Record.dataset))
    )
    return (await db.execute(query)).unique().scalars().all()


async def delete_suggestions_by_record_ids(db: AsyncSession, record_ids: Iterable[UUID]) -> None:
    await db.execute(sql.delete(Suggestion).filter(Suggestion.record_id.in_(record_ids)))


async def fetch_records_by_ids_as_dict(
    db: AsyncSession, dataset: Dataset, record_ids: Sequence[UUID]
) -> Dict[UUID, Record]:
    records_by_ids = await list_dataset_records_by_ids(db, dataset.id, record_ids)
    return {record.id: record for record in records_by_ids}


async def fetch_records_by_external_ids_as_dict(
    db: AsyncSession, dataset: Dataset, external_ids: Sequence[str]
) -> Dict[str, Record]:
    records_by_external_ids = await list_dataset_records_by_external_ids(db, dataset.id, external_ids)
    return {record.external_id: record for record in records_by_external_ids}
