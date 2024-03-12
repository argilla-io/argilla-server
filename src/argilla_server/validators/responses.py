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

from argilla_server.enums import QuestionType
from argilla_server.models import Record
from argilla_server.schemas.v1.responses import ResponseCreate
from argilla_server.validators.response_values import (
    LabelSelectionQuestionResponseValueValidator,
    MultiLabelSelectionQuestionResponseValueValidator,
    RankingQuestionResponseValueValidator,
    RatingQuestionResponseValueValidator,
    SpanQuestionResponseValueValidator,
    TextQuestionResponseValueValidator,
)


class ResponseCreateValidator:
    def __init__(self, response_create: ResponseCreate) -> None:
        self._response_create = response_create

    def validate_for(self, record: Record) -> None:
        self._validate_values_are_present_when_submitted()
        self._validate_required_questions_have_values(record)
        self._validate_values_have_configured_questions(record)
        self._validate_values(record)

    def _validate_values_are_present_when_submitted(self) -> None:
        if self._response_create.is_submitted and not self._response_create.values:
            raise ValueError("missing response values for submitted response")

    def _validate_required_questions_have_values(self, record: Record) -> None:
        for question in record.dataset.questions:
            if (
                self._response_create.is_submitted
                and question.required
                and question.name not in self._response_create.values
            ):
                raise ValueError(f"missing response value for required question with name={question.name}")

    def _validate_values_have_configured_questions(self, record: Record) -> None:
        question_names = [question.name for question in record.dataset.questions]

        for value_question_name in self._response_create.values or []:
            if value_question_name not in question_names:
                raise ValueError(f"found response value for non configured question with name={value_question_name!r}")

    def _validate_values(self, record: Record) -> None:
        if not self._response_create.values:
            return

        for question in record.dataset.questions:
            if question_response := self._response_create.values.get(question.name):
                if question.type == QuestionType.text:
                    TextQuestionResponseValueValidator(question_response.value).validate()
                elif question.type == QuestionType.label_selection:
                    LabelSelectionQuestionResponseValueValidator(question_response.value).validate_for(
                        question.parsed_settings
                    )
                elif question.type == QuestionType.multi_label_selection:
                    MultiLabelSelectionQuestionResponseValueValidator(question_response.value).validate_for(
                        question.parsed_settings
                    )
                elif question.type == QuestionType.rating:
                    RatingQuestionResponseValueValidator(question_response.value).validate_for(question.parsed_settings)
                elif question.type == QuestionType.ranking:
                    RankingQuestionResponseValueValidator(question_response.value).validate_for(
                        self._response_create.status, question.parsed_settings
                    )
                elif question.type == QuestionType.span:
                    SpanQuestionResponseValueValidator(question_response.value).validate_for(
                        question.parsed_settings, record
                    )
                else:
                    raise ValueError(
                        f"unknown question type f{question.type!r} for question with name f{question.name}"
                    )
