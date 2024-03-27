from uuid import UUID

import pytest
from httpx import AsyncClient
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.enums import DatasetStatus
from argilla_server.models import Dataset, Record
from tests.factories import (
    DatasetFactory,
    TextFieldFactory,
    TermsMetadataPropertyFactory,
    RecordFactory,
)


@pytest.mark.asyncio
class TestCreateDatasetRecordsBulk:

    def url(self, dataset_id: UUID) -> str:
        return f"/api/v1/datasets/{dataset_id}/records/bulk"

    async def test_dataset(self, **kwargs) -> Dataset:
        dataset = await DatasetFactory.create(status=DatasetStatus.ready, **kwargs)

        await self._configure_dataset_fields(dataset)
        await self._configure_dataset_metadata_properties(dataset)

        return dataset

    @pytest.mark.parametrize(
        "record_create",
        [
            {
                "fields": {
                    "prompt": "Does exercise help reduce stress?",
                    "response": "Exercise can definitely help reduce stress.",
                },
                "metadata": {"terms_metadata": ["A", "B", "C"]},
            },
            {
                "fields": {
                    "prompt": "Does exercise help reduce stress?",
                    "response": "Exercise can definitely help reduce stress.",
                },
                "metadata": {"terms_metadata": "A"},
                "external_id": "external-id-1",
            },
            {
                "fields": {
                    "prompt": "Does exercise help reduce stress?",
                    "response": "Exercise can definitely help reduce stress.",
                },
                "external_id": "external-id-2",
            },
        ],
    )
    async def test_create_dataset_records(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict, record_create: dict
    ):
        dataset = await self.test_dataset()

        response = await async_client.post(
            self.url(dataset.id), headers=owner_auth_header, json={"items": [record_create]}
        )

        assert response.status_code == 200
        assert (await db.execute(select(func.count(Record.id)))).scalar_one() == 1
        record = (await db.execute(select(Record))).scalar_one()

        response_json = response.json()
        assert response_json == {
            "items": [
                {
                    "id": str(record.id),
                    "dataset_id": str(dataset.id),
                    "external_id": record.external_id,
                    "fields": record.fields,
                    "metadata": record.metadata_,
                    "inserted_at": record.inserted_at.isoformat(),
                    "updated_at": record.updated_at.isoformat(),
                }
            ]
        }

    @pytest.mark.parametrize("metadata", [{"terms_metadata": "b"}, {"terms_metadata": ["c", "a"]}, {}, None])
    async def test_update_record_metadata_by_id(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict, metadata: dict
    ) -> None:
        dataset = await self.test_dataset()
        records = await RecordFactory.create_batch(dataset=dataset, size=100)

        response = await async_client.post(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={"items": [{"id": str(record.id), "metadata": metadata} for record in records]},
        )

        assert response.status_code == 200
        assert (await db.execute(select(func.count(Record.id)))).scalar_one() == len(records)
        updated_records = (await db.execute(select(Record))).scalars().all()
        for record in updated_records:
            assert record.metadata_ == metadata

    @pytest.mark.parametrize("metadata", [{"terms_metadata": "b"}, {"terms_metadata": ["c", "a"]}, {}, None])
    async def test_update_record_metadata_by_external_id(
        self, async_client: AsyncClient, db: AsyncSession, owner_auth_header: dict, metadata: dict
    ):
        dataset = await self.test_dataset()
        records = await RecordFactory.create_batch(dataset=dataset, size=100)

        response = await async_client.post(
            self.url(dataset.id),
            headers=owner_auth_header,
            json={
                "items": [{"external_id": record.external_id, "metadata": metadata} for record in records],
            },
        )

        assert response.status_code == 200
        assert (await db.execute(select(func.count(Record.id)))).scalar_one() == len(records)
        updated_records = (await db.execute(select(Record))).scalars().all()
        for record in updated_records:
            assert record.metadata_ == metadata

    async def _configure_dataset_metadata_properties(self, dataset):
        await TermsMetadataPropertyFactory.create(name="terms_metadata", dataset=dataset)

        await dataset.awaitable_attrs.metadata_properties

    async def _configure_dataset_fields(self, dataset):
        await TextFieldFactory.create(name="prompt", dataset=dataset)
        await TextFieldFactory.create(name="response", dataset=dataset)

        await dataset.awaitable_attrs.fields
