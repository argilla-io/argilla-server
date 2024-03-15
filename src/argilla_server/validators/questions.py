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
from argilla_server.models.database import Dataset
from argilla_server.schemas.v1.questions import QuestionCreate


class QuestionCreateValidator:
    def __init__(self, question_create: QuestionCreate):
        self._question_create = question_create

    def validate_for(self, dataset: Dataset):
        self._validate_dataset_is_not_ready(dataset)
        self._validate_span_question_settings(dataset)

    def _validate_dataset_is_not_ready(self, dataset):
        if dataset.is_ready:
            raise ValueError("questions cannot be created for a published dataset")

    def _validate_span_question_settings(self, dataset: Dataset):
        if self._question_create.settings.type != QuestionType.span:
            return

        field = self._question_create.settings.field
        field_names = [field.name for field in dataset.fields]

        if field not in field_names:
            raise ValueError(f"'{field}' is not a valid field name.\nValid field names are {field_names!r}")

        for question in dataset.questions:
            if question.type == QuestionType.span and field == question.parsed_settings.field:
                raise ValueError(f"'{field}' is already used by span question with id '{question.id}'")
