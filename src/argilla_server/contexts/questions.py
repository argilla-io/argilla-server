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

from typing import List, Union
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import argilla_server.errors.future as errors
from argilla_server.enums import QuestionType
from argilla_server.models import (
    Dataset,
    LabelSelectionQuestionSettings,
    Question,
    QuestionSettings,
    User,
)
from argilla_server.policies import QuestionPolicyV1, authorize
from argilla_server.schemas.v1.questions import (
    LabelSelectionSettingsUpdate,
    QuestionCreate,
    QuestionSettingsUpdate,
    QuestionUpdate,
    SpanQuestionSettingsCreate,
)


class InvalidQuestionSettings(Exception):
    pass


def _validate_settings_type(settings: QuestionSettings, settings_update: QuestionSettingsUpdate):
    if settings.type != settings_update.type:
        raise InvalidQuestionSettings(
            f"Question type cannot be changed. Expected '{settings.type}' but got '{settings_update.type}'"
        )


def _validate_label_options(settings: LabelSelectionQuestionSettings, settings_update: LabelSelectionSettingsUpdate):
    # TODO: Validate visible_options on update
    if settings_update.options is None:
        return

    if len(settings.options) != len(settings_update.options):
        raise InvalidQuestionSettings(
            "The number of options cannot be modified. "
            f"Expected {len(settings.options)} but got {len(settings_update.options)}"
        )

    sorted_options = sorted(settings.options, key=lambda option: option.value)
    sorted_update_options = sorted(settings_update.options, key=lambda option: option.value)

    unexpected_options: List[str] = []
    for option, update_option in zip(sorted_options, sorted_update_options):
        if option.value != update_option.value:
            unexpected_options.append(update_option.value)

    if unexpected_options:
        raise InvalidQuestionSettings(
            f"The option values cannot be modified. " f"Found unexpected option values: {unexpected_options!r}"
        )


def _validate_question_settings(
    question_settings: QuestionSettings,
    question_update_settings: QuestionSettingsUpdate,
) -> None:
    _validate_settings_type(question_settings, question_update_settings)

    if question_settings.type in [QuestionType.label_selection, QuestionType.multi_label_selection, QuestionType.span]:
        _validate_label_options(question_settings, question_update_settings)


async def get_question_by_id(db: AsyncSession, question_id: UUID) -> Union[Question, None]:
    return (
        await db.execute(select(Question).filter_by(id=question_id).options(selectinload(Question.dataset)))
    ).scalar_one_or_none()


async def get_question_by_name_and_dataset_id(db: AsyncSession, name: str, dataset_id: UUID) -> Union[Question, None]:
    return (await db.execute(select(Question).filter_by(name=name, dataset_id=dataset_id))).scalar_one_or_none()


async def get_question_by_name_and_dataset_id_or_raise(db: AsyncSession, name: str, dataset_id: UUID) -> Question:
    question = await get_question_by_name_and_dataset_id(db, name, dataset_id)
    if question is None:
        raise errors.NotFoundError(f"Question with name `{name}` not found for dataset with id `{dataset_id}`")

    return question


def _validate_question_before_create(dataset: Dataset, question_create: QuestionCreate) -> None:
    if question_create.settings.type == QuestionType.span:
        _validate_span_question_settings_before_create(dataset, question_create.settings)


def _validate_question_before_update(question: Question, question_update: QuestionUpdate) -> None:
    if question_update.settings:
        _validate_question_settings(question.parsed_settings, question_update.settings)


def _validate_span_question_settings_before_create(
    dataset: Dataset, span_question_settings_create: SpanQuestionSettingsCreate
) -> None:
    field = span_question_settings_create.field
    field_names = [field.name for field in dataset.fields]

    if field not in field_names:
        raise ValueError(f"'{field}' is not a valid field name.\nValid field names are {field_names!r}")

    for question in dataset.questions:
        if question.type == QuestionType.span and field == question.parsed_settings.field:
            raise ValueError(f"'{field}' is already used by span question with id '{question.id}'")


async def create_question(db: AsyncSession, dataset: Dataset, question_create: QuestionCreate) -> Question:
    if dataset.is_ready:
        raise ValueError("Question cannot be created for a published dataset")

    _validate_question_before_create(dataset, question_create)

    return await Question.create(
        db,
        name=question_create.name,
        title=question_create.title,
        description=question_create.description,
        required=question_create.required,
        settings=question_create.settings.dict(),
        dataset_id=dataset.id,
    )


async def update_question(
    db: AsyncSession, question_id: UUID, question_update: QuestionUpdate, current_user: User
) -> Question:
    question = await get_question_by_id(db, question_id)
    if not question:
        raise errors.NotFoundError()

    await authorize(current_user, QuestionPolicyV1.update(question))

    _validate_question_before_update(question, question_update)

    params = question_update.dict(exclude_unset=True)
    return await question.update(db, **params)


async def delete_question(db: AsyncSession, question: Question) -> Question:
    if question.dataset.is_ready:
        raise ValueError("Questions cannot be deleted for a published dataset")

    return await question.delete(db)
