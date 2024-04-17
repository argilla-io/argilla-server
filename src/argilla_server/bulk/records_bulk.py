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
from typing import Dict, List, Sequence, Tuple, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from argilla_server.contexts.accounts import fetch_users_by_ids_as_dict
from argilla_server.contexts.records import (
    delete_suggestions_by_record_ids,
    fetch_records_by_external_ids_as_dict,
    fetch_records_by_ids_as_dict,
)
from argilla_server.models import Dataset, Question, Record, Response, Suggestion, Vector, VectorSettings
from argilla_server.schemas.v1.records import RecordCreate
from argilla_server.schemas.v1.records_bulk import (
    RecordsBulk,
    RecordsBulkCreate,
    RecordsBulkUpsert,
    RecordsBulkWithUpdateInfo,
    RecordUpsert,
)
from argilla_server.schemas.v1.responses import UserResponseCreate
from argilla_server.schemas.v1.suggestions import SuggestionCreate
from argilla_server.search_engine import SearchEngine
from argilla_server.validators.records_bulk import RecordsBulkCreateValidator, RecordsBulkUpsertValidator
from argilla_server.validators.responses import ResponseCreateValidator
from argilla_server.validators.suggestions import SuggestionCreateValidator
from argilla_server.validators.vectors import VectorValidator


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
            await _preload_records_relationships_before_index(self._db, records)
            await self._search_engine.index_records(dataset, records)

        await self._db.commit()
        return RecordsBulk(items=records)

    async def _upsert_records_relationships(self, records: List[Record], records_create: List[RecordCreate]) -> None:

        records_and_suggestions = list(zip(records, [r.suggestions for r in records_create]))
        records_and_responses = list(zip(records, [r.responses for r in records_create]))
        records_and_vectors = list(zip(records, [r.vectors for r in records_create]))

        await asyncio.gather(
            _upsert_records_suggestions(self._db, records_and_suggestions),
            _upsert_records_responses(self._db, records_and_responses),
            _upsert_records_vectors(self._db, records_and_vectors),
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

            await _preload_records_relationships_before_index(self._db, records)
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

        records_by_external_id = await fetch_records_by_external_ids_as_dict(
            self._db, dataset, [r.external_id for r in records_upsert]
        )
        records_by_id = await fetch_records_by_ids_as_dict(
            self._db, dataset, [r.id for r in records_upsert if r.id not in records_by_external_id]
        )

        return {**records_by_external_id, **records_by_id}


async def _preload_records_relationships_before_index(db: "AsyncSession", records: Sequence[Record]) -> None:
    await db.execute(
        select(Record)
        .filter(Record.id.in_([record.id for record in records]))
        .options(
            selectinload(Record.responses).selectinload(Response.user),
            selectinload(Record.suggestions).selectinload(Suggestion.question),
            selectinload(Record.vectors),
        )
    )


async def _upsert_records_suggestions(
    db: AsyncSession, records_and_suggestions: List[Tuple[Record, List[SuggestionCreate]]]
) -> List[Suggestion]:

    # TODO: This should be removed and aligned to the rest of the the upsert relationships
    await delete_suggestions_by_record_ids(
        db, set([record.id for record, suggestions in records_and_suggestions if suggestions is not None])
    )

    upsert_many_suggestions = []
    for idx, (record, suggestions) in enumerate(records_and_suggestions):
        try:
            for suggestion_create in suggestions or []:
                try:
                    question = _get_question_by_id(record.dataset, suggestion_create.question_id)
                    if question is None:
                        raise ValueError(f"question_id={suggestion_create.question_id} does not exist")

                    SuggestionCreateValidator(suggestion_create).validate_for(question.parsed_settings, record)
                    upsert_many_suggestions.append(dict(**suggestion_create.dict(), record_id=record.id))
                except ValueError as ex:
                    raise ValueError(f"suggestion for question_id={suggestion_create.question_id} is not valid: {ex}")
        except ValueError as ex:
            raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex

    if not upsert_many_suggestions:
        return []

    return await Suggestion.upsert_many(
        db,
        objects=upsert_many_suggestions,
        constraints=[Suggestion.record_id, Suggestion.question_id],
        autocommit=False,
    )


async def _upsert_records_responses(
    db: AsyncSession, records_and_responses: List[Tuple[Record, List[UserResponseCreate]]]
) -> List[Response]:

    user_ids = [response.user_id for _, responses in records_and_responses for response in responses or []]
    users_by_id = await fetch_users_by_ids_as_dict(db, user_ids)

    upsert_many_responses = []
    for idx, (record, responses) in enumerate(records_and_responses):
        try:
            for response_create in responses or []:
                if response_create.user_id not in users_by_id:
                    raise ValueError(f"user with id {response_create.user_id} not found")

                ResponseCreateValidator(response_create).validate_for(record)
                upsert_many_responses.append(dict(**response_create.dict(), record_id=record.id))
        except ValueError as ex:
            raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex

    if not upsert_many_responses:
        return []

    return await Response.upsert_many(
        db,
        objects=upsert_many_responses,
        constraints=[Response.record_id, Response.user_id],
        autocommit=False,
    )


async def _upsert_records_vectors(db, records_and_vectors: List[Tuple[Record, Dict[str, List[float]]]]) -> List[Vector]:

    upsert_many_vectors = []
    for idx, (record, vectors) in enumerate(records_and_vectors):
        try:
            for name, value in (vectors or {}).items():
                try:
                    settings = _get_vector_settings_by_name(record.dataset, name)
                    if not settings:
                        raise ValueError(f"vector with name={name} does not exist for dataset_id={record.dataset.id}")

                    VectorValidator(value).validate_for(settings)
                    upsert_many_vectors.append(dict(value=value, record_id=record.id, vector_settings_id=settings.id))
                except ValueError as ex:
                    raise ValueError(f"vector with name={name} is not valid: {ex}") from ex
        except ValueError as ex:
            raise ValueError(f"Record at position {idx} is not valid because {ex}") from ex

    if not upsert_many_vectors:
        return []

    return await Vector.upsert_many(
        db,
        objects=upsert_many_vectors,
        constraints=[Vector.record_id, Vector.vector_settings_id],
        autocommit=False,
    )


def _get_question_by_id(dataset: Dataset, question_id: UUID) -> Union[Question, None]:
    for question in dataset.questions:
        if question.id == question_id:
            return question


def _get_vector_settings_by_name(dataset: Dataset, name: str) -> Union[VectorSettings, None]:
    for vector_settings in dataset.vectors_settings:
        if vector_settings.name == name:
            return vector_settings
