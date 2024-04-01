from typing import List, Union, Iterable, Sequence, Dict
from uuid import UUID

from sqlalchemy import sql, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from argilla_server.contexts import accounts
from argilla_server.models import Record, Suggestion, Response, Vector, Dataset, Question
from argilla_server.schemas.v1.records import RecordCreate, RecordUpdateWithId, RecordUpsert
from argilla_server.validators.responses import ResponseCreateValidator
from argilla_server.validators.suggestions import SuggestionCreateValidator
from argilla_server.validators.vectors import VectorValidator


def check_is_ready_dataset(dataset: Dataset) -> None:
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


async def upsert_records_suggestions(
    db: AsyncSession, records: List[Record], records_upsert: List[Union[RecordCreate, RecordUpdateWithId, RecordUpsert]]
) -> List[Suggestion]:

    records_ids_with_suggestions = [
        record.id for record, record_upsert in zip(records, records_upsert) if record_upsert.suggestions is not None
    ]

    await _delete_suggestions_by_record_ids(db, set(records_ids_with_suggestions))

    upsert_many_suggestions = []
    for idx, (record, record_upsert) in enumerate(zip(records, records_upsert)):
        if record_upsert.suggestions is None:
            continue
        try:
            for suggestion_create in record_upsert.suggestions:
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
    db: AsyncSession, records: List[Record], records_upsert: List[Union[RecordCreate, RecordUpdateWithId, RecordUpsert]]
) -> List[Response]:

    users = await accounts.list_users_by_ids(
        db, set([response.user_id for record in records_upsert for response in record.responses or []])
    )
    users_by_id = {user.id: user for user in users}

    upsert_many_responses = []
    for idx, (record, record_upsert) in enumerate(zip(records, records_upsert)):
        try:
            for response_create in record_upsert.responses or []:
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


async def upsert_records_vectors(
    db, records: List[Record], records_upsert: List[Union[RecordCreate, RecordUpdateWithId, RecordUpsert]]
) -> List[Vector]:

    upsert_many_vectors = []
    for idx, (record, records_upsert) in enumerate(zip(records, records_upsert)):
        try:
            for name, value in (records_upsert.vectors or {}).items():
                try:
                    settings = record.dataset.vector_settings_by_name(name)
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


async def _delete_suggestions_by_record_ids(db: AsyncSession, record_ids: Iterable[UUID]) -> None:
    await db.execute(sql.delete(Suggestion).filter(Suggestion.record_id.in_(record_ids)))
