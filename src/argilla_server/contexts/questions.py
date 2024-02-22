from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.contexts import datasets
from argilla_server.enums import QuestionType
from argilla_server.models import (
    LabelSelectionQuestionSettings,
    QuestionSettings,
    User,
)
from argilla_server.policies import QuestionPolicyV1, authorize
from argilla_server.schemas.v1.questions import (
    LabelSelectionSettingsUpdate,
    QuestionSettingsUpdate,
    QuestionUpdate,
)


class NotFoundError(Exception):
    pass


class UpdateValidationError(Exception):
    pass


def _validate_settings_type(settings: QuestionSettings, settings_update: QuestionSettingsUpdate):
    if settings.type != settings_update.type:
        raise UpdateValidationError(
            f"Question type cannot be changed. Expected '{settings.type}' but got '{settings_update.type}'"
        )


def _validate_label_options(settings: LabelSelectionQuestionSettings, settings_update: LabelSelectionSettingsUpdate):
    if settings_update.options is None:
        return

    if len(settings.options) != len(settings_update.options):
        raise UpdateValidationError(
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
        raise UpdateValidationError(
            f"The option values cannot be modified. " f"Found unexpected option values: {unexpected_options!r}"
        )


def _validate_question_settings(
    question_settings: QuestionSettings,
    question_update_settings: QuestionSettingsUpdate,
) -> None:
    _validate_settings_type(question_settings, question_update_settings)

    if question_settings.type in [QuestionType.label_selection, QuestionType.multi_label_selection]:
        _validate_label_options(question_settings, question_update_settings)


async def update_question(db: AsyncSession, question_id: UUID, question_update: QuestionUpdate, current_user: User):
    question = await datasets.get_question_by_id(db, question_id)
    if not question:
        raise NotFoundError()

    await authorize(current_user, QuestionPolicyV1.update(question))

    if question_update.settings:
        _validate_question_settings(question.parsed_settings, question_update.settings)

    params = question_update.dict(exclude_unset=True)
    return await question.update(db, **params)
