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

from uuid import UUID

import pytest
from httpx import AsyncClient

from argilla_server.enums import QuestionType
from tests.factories import LabelSelectionQuestionFactory, TextQuestionFactory, SpanQuestionFactory


@pytest.mark.asyncio
class TestUpdateQuestion:
    def url(self, question_id: UUID) -> str:
        return f"/api/v1/questions/{question_id}"

    async def test_update_question_with_different_type(self, async_client: AsyncClient, owner_auth_header: dict):
        question = await TextQuestionFactory.create()

        response = await async_client.patch(
            self.url(question.id),
            headers=owner_auth_header,
            json={
                "settings": {
                    "type": QuestionType.label_selection,
                },
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "question type cannot be changed. expected 'text' but got 'label_selection'"
        }

    async def test_update_question_with_different_number_of_options(
        self, async_client: AsyncClient, owner_auth_header: dict
    ):
        question = await LabelSelectionQuestionFactory.create()

        response = await async_client.patch(
            self.url(question.id),
            headers=owner_auth_header,
            json={
                "settings": {
                    "type": QuestionType.label_selection,
                    "options": [
                        {"value": "label-a", "text": "Label A"},
                        {"value": "label-b", "text": "Label B"},
                        {"value": "label-c", "text": "Label C"},
                        {"value": "label-d", "text": "Label D"},
                    ],
                },
            },
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "the number of options cannot be modified. expected 3 but got 4"}

    async def test_update_question_with_different_options(self, async_client: AsyncClient, owner_auth_header: dict):
        question = await LabelSelectionQuestionFactory.create()

        response = await async_client.patch(
            self.url(question.id),
            headers=owner_auth_header,
            json={
                "settings": {
                    "type": QuestionType.label_selection,
                    "options": [
                        {"value": "label-a", "text": "Label A"},
                        {"value": "label-b", "text": "Label B"},
                        {"value": "label-c", "text": "Label C"},
                    ],
                },
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "the option values cannot be modified. found unexpected option values: ['label-a', 'label-b', 'label-c']"
        }

    async def test_update_question_with_more_visible_options_than_allowed(
        self, async_client: AsyncClient, owner_auth_header: dict
    ):
        question = await LabelSelectionQuestionFactory.create()

        response = await async_client.patch(
            self.url(question.id),
            headers=owner_auth_header,
            json={
                "settings": {
                    "type": QuestionType.label_selection,
                    "visible_options": 4,
                },
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "the value for 'visible_options' must be less or equal to the number of items in 'options' (3)"
        }

    async def test_update_span_question_with_unsupported_allow_overlapping_value(
        self, async_client: AsyncClient, owner_auth_header: dict
    ):
        question = await SpanQuestionFactory.create(
            settings={
                "type": QuestionType.span.value,
                "field": "field-a",
                "options": [
                    {"value": "label-a", "text": "Label A", "description": "Label A description"},
                    {"value": "label-b", "text": "Label B", "description": "Label B description"},
                    {"value": "label-c", "text": "Label C", "description": "Label C description"},
                ],
                "allow_overlapping": True,
            }
        )

        response = await async_client.patch(
            self.url(question.id),
            headers=owner_auth_header,
            json={
                "settings": {
                    "type": QuestionType.span,
                    "allow_overlapping": False
                },
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "'allow_overlapping' can't be disabled because responses may become inconsistent"
        }
