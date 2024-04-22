from uuid import UUID

import pytest
from httpx import AsyncClient
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.enums import DatasetStatus, QuestionType
from argilla_server.models import Dataset, Suggestion
from tests.factories import (
    DatasetFactory,
    TextFieldFactory,
    LabelSelectionQuestionFactory,
    RecordFactory,
    SuggestionFactory,
    TextQuestionFactory,
)


@pytest.mark.asyncio
class TestDatasetRecordsBulkWithSuggestions:

    def url(self, dataset_id: UUID) -> str:
        return f"/api/v1/datasets/{dataset_id}/records/bulk"

    async def test_dataset(self, **kwargs) -> Dataset:
        dataset = await DatasetFactory.create(status=DatasetStatus.ready, **kwargs)

        await self._configure_dataset_fields(dataset)
        await self._configure_dataset_questions(dataset)

        return dataset

    async def _configure_dataset_fields(self, dataset: Dataset):
        await TextFieldFactory.create(name="prompt", dataset=dataset)
        await TextFieldFactory.create(name="response", dataset=dataset)

        await dataset.awaitable_attrs.fields

    async def test_create_record_with_suggestions_in_bulk(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await self.test_dataset()
        question_id = str(dataset.question_by_name("label").id)

        response = await async_client.post(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={
                "items": [
                    {
                        "fields": {
                            "prompt": "Does exercise help reduce stress?",
                            "response": "Exercise can definitely help reduce stress.",
                        },
                        "suggestions": [
                            {"question_id": question_id, "value": "label-a"},
                        ],
                    },
                ]
            },
        )

        assert response.status_code == 201, response.json()
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar_one() == 1
        suggestion = (await db.execute(select(Suggestion))).scalar_one()

        response_json = response.json()
        suggestions = [suggestion for item in response_json["items"] for suggestion in item["suggestions"]]
        assert suggestions == [
            {
                "id": str(suggestion.id),
                "question_id": question_id,
                "value": "label-a",
                "score": suggestion.score,
                "type": suggestion.type,
                "agent": suggestion.agent,
                "inserted_at": suggestion.inserted_at.isoformat(),
                "updated_at": suggestion.updated_at.isoformat(),
            },
        ]

    async def test_create_suggestions_with_record_update_in_bulk(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await self.test_dataset()
        record = await RecordFactory.create(dataset=dataset, fields={"prompt": "Does exercise help reduce stress?"})
        question_id = str(dataset.question_by_name("label").id)

        response = await async_client.put(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={
                "items": [
                    {
                        "id": str(record.id),
                        "suggestions": [
                            {"question_id": question_id, "value": "label-a"},
                        ],
                    },
                ]
            },
        )

        assert response.status_code == 200, response.json()
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar_one() == 1
        suggestion = (await db.execute(select(Suggestion))).scalar_one()

        response_json = response.json()
        suggestions = [suggestion for item in response_json["items"] for suggestion in item["suggestions"]]
        assert suggestions == [
            {
                "id": str(suggestion.id),
                "question_id": question_id,
                "value": "label-a",
                "score": suggestion.score,
                "type": suggestion.type,
                "agent": suggestion.agent,
                "inserted_at": suggestion.inserted_at.isoformat(),
                "updated_at": suggestion.updated_at.isoformat(),
            },
        ]

    async def test_upsert_record_with_suggestions_in_bulk(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await self.test_dataset()
        question_id = str(dataset.question_by_name("label").id)

        response = await async_client.put(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={
                "items": [
                    {
                        "fields": {
                            "prompt": "Does exercise help reduce stress?",
                            "response": "Exercise can definitely help reduce stress.",
                        },
                        "suggestions": [
                            {"question_id": question_id, "value": "label-a"},
                        ],
                    },
                ]
            },
        )

        assert response.status_code == 200, response.json()
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar_one() == 1
        suggestion = (await db.execute(select(Suggestion))).scalar_one()

        response_json = response.json()
        suggestions = [suggestion for item in response_json["items"] for suggestion in item["suggestions"]]
        assert suggestions == [
            {
                "id": str(suggestion.id),
                "question_id": question_id,
                "value": "label-a",
                "score": suggestion.score,
                "type": suggestion.type,
                "agent": suggestion.agent,
                "inserted_at": suggestion.inserted_at.isoformat(),
                "updated_at": suggestion.updated_at.isoformat(),
            },
        ]

    async def test_update_record_suggestions_in_bulk(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict
    ):
        dataset = await self.test_dataset()
        question = dataset.question_by_name("label")
        record = await RecordFactory.create(dataset=dataset, fields={"prompt": "Does exercise help reduce stress?"})
        suggestion = await SuggestionFactory.create(record=record, question=question, value="label-a")

        response = await async_client.put(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={
                "items": [
                    {
                        "id": str(record.id),
                        "suggestions": [
                            {"question_id": str(question.id), "value": "label-b"},
                        ],
                    },
                ]
            },
        )

        assert response.status_code == 200, response.json()
        assert (await db.execute(select(func.count(Suggestion.id)))).scalar_one() == 1

        response_suggestions = response.json()["items"][0]["suggestions"]
        assert response_suggestions == [
            {
                "id": str(suggestion.id),
                "question_id": str(question.id),
                "value": "label-b",
                "score": suggestion.score,
                "type": suggestion.type,
                "agent": suggestion.agent,
                "inserted_at": suggestion.inserted_at.isoformat(),
                "updated_at": suggestion.updated_at.isoformat(),
            },
        ]

        suggestion = (await db.execute(select(Suggestion))).scalar_one()
        assert suggestion.value == "label-b"

    async def test_create_record_with_suggestions_in_bulk_with_wrong_question(
        self, async_client: AsyncClient, owner_auth_header: dict
    ):
        dataset = await self.test_dataset()
        other_question = await TextQuestionFactory.create(name="other-question")

        response = await async_client.post(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={
                "items": [
                    {
                        "fields": {
                            "prompt": "Does exercise help reduce stress?",
                            "response": "Exercise can definitely help reduce stress.",
                        },
                        "suggestions": [
                            {"question_id": str(other_question.id), "value": "label-c"},
                        ],
                    },
                ]
            },
        )

        assert response.status_code == 422, response.json()
        assert response.json() == {
            "detail": f"Record at position 0 is not valid because suggestion for question_id={other_question.id} "
            f"is not valid: question_id={other_question.id} does not exist"
        }

    async def test_create_record_with_suggestions_in_bulk_with_wrong_value(
        self, async_client: AsyncClient, owner_auth_header: dict
    ):
        dataset = await self.test_dataset()
        question_id = str(dataset.question_by_name("label").id)

        response = await async_client.post(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={
                "items": [
                    {
                        "fields": {
                            "prompt": "Does exercise help reduce stress?",
                            "response": "Exercise can definitely help reduce stress.",
                        },
                        "suggestions": [
                            {"question_id": question_id, "value": "wrong-label"},
                        ],
                    },
                ]
            },
        )

        assert response.status_code == 422, response.json()
        assert response.json() == {
            "detail": f"Record at position 0 is not valid because suggestion for question_id={question_id} "
            f"is not valid: 'wrong-label' is not a valid label for label selection question.\n"
            "Valid labels are: ['label-a', 'label-b']"
        }

    async def _configure_dataset_questions(self, dataset: Dataset):
        await LabelSelectionQuestionFactory.create(
            dataset=dataset,
            name="label",
            settings={
                "type": QuestionType.label_selection,
                "options": [
                    {"value": "label-a", "text": "Label A", "description": "Label A description"},
                    {"value": "label-b", "text": "Label B", "description": "Label B description"},
                ],
            },
        )

        await dataset.awaitable_attrs.questions
