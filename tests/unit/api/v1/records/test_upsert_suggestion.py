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

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

import pytest
from argilla_server.enums import SuggestionType
from argilla_server.models import Suggestion
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import DatasetFactory, RecordFactory, SpanQuestionFactory, TextQuestionFactory


@pytest.mark.asyncio
class TestUpsertSuggestion:
    def url(self, record_id: UUID) -> str:
        return f"/api/v1/records/{record_id}/suggestions"

    @pytest.mark.parametrize(
        "agent", ["a", "A", "0", "gpt 3.5", "gpt-3.5-turbo", "argilla/zephyr-7b", "ft:gpt-3.5-turbo"]
    )
    async def test_upsert_suggestion_with_valid_agent(
        self, async_client: AsyncClient, owner_auth_header: dict, agent: str
    ):
        record = await RecordFactory.create()
        question = await TextQuestionFactory.create(dataset=record.dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(question.id),
                "type": SuggestionType.model,
                "value": "value",
                "agent": agent,
                "score": 1.0,
            },
        )

        assert response.status_code == 201

    @pytest.mark.parametrize("agent", ["", " ", "  ", "-", "_", ":", ".", "/", ","])
    async def test_upsert_suggestion_with_invalid_agent(
        self, async_client: AsyncClient, owner_auth_header: dict, agent: str
    ):
        response = await async_client.put(
            self.url(uuid4()),
            headers=owner_auth_header,
            json={
                "question_id": str(uuid4()),
                "type": SuggestionType.model,
                "value": "value",
                "agent": agent,
                "score": 1.0,
            },
        )

        assert response.status_code == 422

    async def test_upsert_suggestion_with_invalid_min_length_agent(
        self, async_client: AsyncClient, owner_auth_header: dict
    ):
        response = await async_client.put(
            self.url(uuid4()),
            headers=owner_auth_header,
            json={
                "question_id": str(uuid4()),
                "type": SuggestionType.model,
                "value": "value",
                "agent": "",
                "score": 1.0,
            },
        )

        assert response.status_code == 422

    async def test_upsert_suggestion_with_invalid_max_length_agent(
        self, async_client: AsyncClient, owner_auth_header: dict
    ):
        response = await async_client.put(
            self.url(uuid4()),
            headers=owner_auth_header,
            json={
                "question_id": str(uuid4()),
                "type": SuggestionType.model,
                "value": "value",
                "agent": "a" * 201,
                "score": 1.0,
            },
        )

        assert response.status_code == 422

    async def test_upsert_suggestion_with_invalid_lower_score(self, async_client: AsyncClient, owner_auth_header: dict):
        response = await async_client.put(
            self.url(uuid4()),
            headers=owner_auth_header,
            json={
                "question_id": str(uuid4()),
                "type": SuggestionType.model,
                "value": "value",
                "agent": "agent",
                "score": -0.1,
            },
        )

        assert response.status_code == 422

    async def test_upsert_suggestion_with_invalid_upper_score(self, async_client: AsyncClient, owner_auth_header: dict):
        response = await async_client.put(
            self.url(uuid4()),
            headers=owner_auth_header,
            json={
                "question_id": str(uuid4()),
                "type": SuggestionType.model,
                "value": "value",
                "agent": "agent",
                "score": 1.1,
            },
        )

        assert response.status_code == 422

    async def test_upsert_suggestion_for_span_question(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 0, "end": 1, "score": 0.2},
                    {"label": "label-b", "start": 2, "end": 3, "score": 1},
                    {"label": "label-c", "start": 4, "end": 5},
                ],
            },
        )

        assert response.status_code == 201
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 1

        response_json = response.json()
        assert await db.get(Suggestion, UUID(response_json["id"]))
        assert response_json == {
            "id": str(UUID(response_json["id"])),
            "question_id": str(span_question.id),
            "type": SuggestionType.model,
            "value": [
                {"label": "label-a", "start": 0, "end": 1, "score": 0.2},
                {"label": "label-b", "start": 2, "end": 3, "score": 1.0},
                {"label": "label-c", "start": 4, "end": 5},
            ],
            "agent": None,
            "score": None,
            "inserted_at": datetime.fromisoformat(response_json["inserted_at"]).isoformat(),
            "updated_at": datetime.fromisoformat(response_json["updated_at"]).isoformat(),
        }

    async def test_upsert_suggestion_for_span_question_with_empty_value(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [],
            },
        )

        assert response.status_code == 201
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 1

        response_json = response.json()
        assert await db.get(Suggestion, UUID(response_json["id"]))
        assert response_json == {
            "id": str(UUID(response_json["id"])),
            "question_id": str(span_question.id),
            "type": SuggestionType.model,
            "value": [],
            "agent": None,
            "score": None,
            "inserted_at": datetime.fromisoformat(response_json["inserted_at"]).isoformat(),
            "updated_at": datetime.fromisoformat(response_json["updated_at"]).isoformat(),
        }

    async def test_upsert_suggestion_for_span_question_with_record_not_providing_required_field(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"other-field": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 0, "end": 1},
                ],
            },
        )

        assert response.status_code == 422, response.json()
        assert response.json() == {"detail": "span question requires record to have field `field-a`"}

        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_invalid_value(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 0, "end": 1},
                    {"invalid": "value"},
                ],
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    @pytest.mark.parametrize("invalid_score", [-0.1, 1.1, "not-a-number"])
    async def test_upsert_suggestion_for_span_question_with_invalid_score(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict, invalid_score: Any
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 0, "end": 1, "score": invalid_score},
                ],
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_start_greater_than_expected(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 5, "end": 6},
                ],
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "span question response value `start` must have a value lower than record field `field-a` length that is `5`"
        }

        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_end_greater_than_expected(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 4, "end": 6},
                ],
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "span question response value `end` must have a value lower or equal than record field `field-a` length that is `5`"
        }

        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_invalid_start(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": -1, "end": 1},
                ],
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_invalid_end(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 0, "end": 0},
                ],
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_equal_start_and_end(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 1, "end": 1},
                ],
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_end_smaller_than_start(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-a", "start": 3, "end": 2},
                ],
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0

    async def test_upsert_suggestion_for_span_question_with_non_existent_label(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        span_question = await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(fields={"field-a": "Hello"}, dataset=dataset)

        response = await async_client.put(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "question_id": str(span_question.id),
                "type": SuggestionType.model,
                "value": [
                    {"label": "label-non-existent", "start": 1, "end": 2},
                ],
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "undefined label 'label-non-existent' for span question.\nValid labels are: ['label-a', 'label-b', 'label-c']"
        }

        assert (await db.execute(select(func.count(Suggestion.id)))).scalar() == 0
