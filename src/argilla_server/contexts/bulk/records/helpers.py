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

from typing import Dict, Iterable, List, Sequence, Tuple, Union
from uuid import UUID

from sqlalchemy import select, sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from argilla_server.contexts import accounts
from argilla_server.models import Dataset, Question, Record, Response, Suggestion, User, Vector, VectorSettings
from argilla_server.schemas.v1.responses import UserResponseCreate
from argilla_server.schemas.v1.suggestions import SuggestionCreate
from argilla_server.validators.responses import ResponseCreateValidator
from argilla_server.validators.suggestions import SuggestionCreateValidator
from argilla_server.validators.vectors import VectorValidator


def check_dataset_is_ready(dataset: Dataset) -> None:
    if not dataset.is_ready:
        raise ValueError("Records cannot be created for a non published dataset")


async def preload_records_relationships_before_index(db: "AsyncSession", records: Sequence[Record]) -> None:
    await db.execute(
        select(Record)
        .filter(Record.id.in_([record.id for record in records]))
        .options(
            selectinload(Record.responses).selectinload(Response.user),
            selectinload(Record.suggestions).selectinload(Suggestion.question),
            selectinload(Record.vectors),
        )
    )


async def fetch_records_by_ids(db: AsyncSession, dataset: Dataset, record_ids: Sequence[UUID]) -> Dict[UUID, Record]:
    records_by_ids = await _list_dataset_records_by_ids(db, dataset.id, record_ids)
    return {record.id: record for record in records_by_ids}


async def fetch_records_by_external_ids(
    db: AsyncSession, dataset: Dataset, external_ids: Sequence[str]
) -> Dict[str, Record]:
    records_by_external_ids = await _list_dataset_records_by_external_ids(db, dataset.id, external_ids)
    return {record.external_id: record for record in records_by_external_ids}


async def upsert_records_suggestions(
    db: AsyncSession, records_and_suggestions: List[Tuple[Record, List[SuggestionCreate]]]
) -> List[Suggestion]:

    # TODO: This should be removed and aligned to the rest of the the upsert relationships
    await _delete_suggestions_by_record_ids(
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


async def upsert_records_responses(
    db: AsyncSession, records_and_responses: List[Tuple[Record, List[UserResponseCreate]]]
) -> List[Response]:

    user_ids = [response.user_id for _, responses in records_and_responses for response in responses or []]
    users_by_id = await _fetch_users_by_ids(db, user_ids)

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


async def upsert_records_vectors(db, records_and_vectors: List[Tuple[Record, Dict[str, List[float]]]]) -> List[Vector]:

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


async def _fetch_users_by_ids(db: AsyncSession, user_ids: List[UUID]) -> Dict[UUID, User]:
    users = await accounts.list_users_by_ids(db, set(user_ids))
    return {user.id: user for user in users}


async def _list_dataset_records_by_external_ids(
    db: AsyncSession, dataset_id: UUID, external_ids: Sequence[str]
) -> Sequence[Record]:

    query = (
        select(Record)
        .filter(Record.external_id.in_(external_ids), Record.dataset_id == dataset_id)
        .options(selectinload(Record.dataset))
    )
    return (await db.execute(query)).unique().scalars().all()


async def _list_dataset_records_by_ids(
    db: AsyncSession, dataset_id: UUID, record_ids: Sequence[UUID]
) -> Sequence[Record]:

    query = select(Record).filter(Record.id.in_(record_ids), Record.dataset_id == dataset_id)
    return (await db.execute(query)).unique().scalars().all()


def _get_question_by_id(dataset: Dataset, question_id: UUID) -> Union[Question, None]:
    for question in dataset.questions:
        if question.id == question_id:
            return question


def _get_vector_settings_by_name(dataset: Dataset, name: str) -> Union[VectorSettings, None]:
    for vector_settings in dataset.vectors_settings:
        if vector_settings.name == name:
            return vector_settings


async def _delete_suggestions_by_record_ids(db: AsyncSession, record_ids: Iterable[UUID]) -> None:
    await db.execute(sql.delete(Suggestion).filter(Suggestion.record_id.in_(record_ids)))
