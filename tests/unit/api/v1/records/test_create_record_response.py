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
from uuid import UUID

import pytest
from argilla_server.enums import QuestionType, ResponseStatusFilter
from argilla_server.models import Response, User
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import DatasetFactory, RecordFactory, SpanQuestionFactory, TextFieldFactory, TextQuestionFactory


@pytest.mark.asyncio
class TestCreateRecordResponse:
    def url(self, record_id: UUID) -> str:
        return f"/api/v1/records/{record_id}/responses"

    async def test_create_record_response_for_span_question(
        self, async_client: AsyncClient, db: AsyncSession, owner: User, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        await TextFieldFactory.create(name="field-a", dataset=dataset)
        await TextFieldFactory.create(name="field-b", dataset=dataset)

        await TextQuestionFactory.create(name="text-question", dataset=dataset)
        await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(dataset=dataset)

        response = await async_client.post(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "values": {
                    "text-question": {"value": "text"},
                    "span-question": {
                        "value": [
                            {"field": "field-a", "label": "label-a", "start": 0, "end": 0},
                            {"field": "field-a", "label": "label-b", "start": 24, "end": 32},
                            {"field": "field-b", "label": "label-c", "start": 32, "end": 45},
                        ],
                    },
                },
                "status": ResponseStatusFilter.submitted,
            },
        )

        assert response.status_code == 201
        assert (await db.execute(select(func.count(Response.id)))).scalar() == 1

        response_body = response.json()
        assert await db.get(Response, UUID(response_body["id"]))
        assert response_body == {
            "id": str(UUID(response_body["id"])),
            "values": {
                "text-question": {"value": "text"},
                "span-question": {
                    "value": [
                        {"field": "field-a", "label": "label-a", "start": 0, "end": 0},
                        {"field": "field-a", "label": "label-b", "start": 24, "end": 32},
                        {"field": "field-b", "label": "label-c", "start": 32, "end": 45},
                    ],
                },
            },
            "status": ResponseStatusFilter.submitted,
            "record_id": str(record.id),
            "user_id": str(owner.id),
            "inserted_at": datetime.fromisoformat(response_body["inserted_at"]).isoformat(),
            "updated_at": datetime.fromisoformat(response_body["updated_at"]).isoformat(),
        }

    async def test_create_record_response_for_span_question_with_invalid_value(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        await TextFieldFactory.create(name="field-a", dataset=dataset)
        await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(dataset=dataset)

        response = await async_client.post(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "values": {
                    "span-question": {
                        "value": [
                            {"field": "field-a", "label": "label-a", "start": 0, "end": 12},
                            {"invalid": "value"},
                        ],
                    },
                },
                "status": ResponseStatusFilter.submitted,
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Response.id)))).scalar() == 0

    async def test_create_record_response_for_span_question_with_invalid_start(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        await TextFieldFactory.create(name="field-a", dataset=dataset)
        await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(dataset=dataset)

        response = await async_client.post(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "values": {
                    "span-question": {
                        "value": [
                            {"field": "field-a", "label": "label-a", "start": -1, "end": 0},
                        ],
                    },
                },
                "status": ResponseStatusFilter.submitted,
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Response.id)))).scalar() == 0

    async def test_create_record_response_for_span_question_with_invalid_end(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        await TextFieldFactory.create(name="field-a", dataset=dataset)
        await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(dataset=dataset)

        response = await async_client.post(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "values": {
                    "span-question": {
                        "value": [
                            {"field": "field-a", "label": "label-a", "start": 0, "end": -1},
                        ],
                    },
                },
                "status": ResponseStatusFilter.submitted,
            },
        )

        assert response.status_code == 422
        assert (await db.execute(select(func.count(Response.id)))).scalar() == 0

    async def test_create_record_response_for_span_question_with_non_existent_field(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        await TextFieldFactory.create(name="field-a", dataset=dataset)
        await TextFieldFactory.create(name="field-b", dataset=dataset)

        await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(dataset=dataset)

        response = await async_client.post(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "values": {
                    "span-question": {
                        "value": [
                            {"field": "field-non-existent", "label": "label-c", "start": 32, "end": 45},
                        ],
                    },
                },
                "status": ResponseStatusFilter.submitted,
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "Undefined field 'field-non-existent' for span question.\nValid fields are: ['field-a', 'field-b']"
        }

        assert (await db.execute(select(func.count(Response.id)))).scalar() == 0

    async def test_create_record_response_for_span_question_with_non_existent_label(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await DatasetFactory.create()

        await TextFieldFactory.create(name="field-a", dataset=dataset)

        await SpanQuestionFactory.create(name="span-question", dataset=dataset)

        record = await RecordFactory.create(dataset=dataset)

        response = await async_client.post(
            self.url(record.id),
            headers=owner_auth_header,
            json={
                "values": {
                    "span-question": {
                        "value": [
                            {"field": "field-a", "label": "label-non-existent", "start": 32, "end": 45},
                        ],
                    },
                },
                "status": ResponseStatusFilter.submitted,
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "Undefined label 'label-non-existent' for span question.\nValid labels are: ['label-a', 'label-b', 'label-c']"
        }

        assert (await db.execute(select(func.count(Response.id)))).scalar() == 0
