import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.models import Dataset
from argilla_server.schemas.v1.records import RecordCreate, RecordUpsert
from argilla_server.schemas.v1.records_bulk import RecordsBulkCreate, RecordsBulkUpsert
from argilla_server.validators.records import RecordsBulkCreateValidator, RecordsBulkUpsertValidator
from tests.factories import DatasetFactory, TextFieldFactory, RecordFactory


@pytest.mark.asyncio
class TestRecordsBulkValidators:

    async def configure_dataset(self) -> Dataset:
        dataset = await DatasetFactory.create(status="ready")

        await TextFieldFactory.create(name="text", dataset=dataset)
        await dataset.awaitable_attrs.fields

        await dataset.awaitable_attrs.metadata_properties

        return dataset

    async def test_records_bulk_create_validator(self, db: AsyncSession):
        dataset = await self.configure_dataset()

        records_create = RecordsBulkCreate(
            items=[
                RecordCreate(fields={"text": "hello world"}, metadata={"source": "test"}),
            ]
        )

        await RecordsBulkCreateValidator(records_create, db).validate_for(dataset)

    async def test_records_validator_with_draft_dataset(self, db: AsyncSession):
        dataset = await DatasetFactory.create(status="draft")

        with pytest.raises(ValueError, match="records cannot be created for a non published dataset"):
            records_create = RecordsBulkCreate(
                items=[
                    RecordCreate(fields={"text": "hello world"}, metadata={"source": "test"}),
                ]
            )
            await RecordsBulkCreateValidator(records_create, db=db).validate_for(dataset)

    async def test_records_bulk_create_validator_with_existing_external_id_in_db(self, db: AsyncSession):
        dataset = await self.configure_dataset()
        created_record = await RecordFactory.create(external_id="1", dataset=dataset)

        records_create = RecordsBulkCreate(
            items=[
                RecordCreate(
                    external_id=created_record.external_id, fields={"text": "hello world"}, metadata={"source": "test"}
                ),
                RecordCreate(fields={"text": "hello world"}, metadata={"source": "test"}),
            ]
        )

        with pytest.raises(ValueError, match="found records with same external ids: 1"):
            await RecordsBulkCreateValidator(records_create, db).validate_for(dataset)

    async def test_records_bulk_create_validator_with_record_errors(self, db: AsyncSession):
        dataset = await self.configure_dataset()
        records_create = RecordsBulkCreate(
            items=[
                RecordCreate(fields={"text": "hello world"}, metadata={"source": "test"}),
                RecordCreate(fields={"wrong-field": "hello world"}),
            ]
        )

        with pytest.raises(
            ValueError,
            match="record at position 1 is not valid because",
        ):
            await RecordsBulkCreateValidator(records_create, db).validate_for(dataset)

    async def test_records_bulk_upsert_validator(self, db: AsyncSession):
        dataset = await self.configure_dataset()

        records_upsert = RecordsBulkUpsert(
            items=[
                RecordUpsert(fields={"text": "hello world"}, metadata={"source": "test"}),
            ]
        )

        RecordsBulkUpsertValidator(records_upsert, db).validate_for(dataset)

    async def test_records_bulk_upsert_validator_with_draft_dataset(self, db: AsyncSession):
        dataset = await DatasetFactory.create(status="draft")

        with pytest.raises(ValueError, match="records cannot be created or updated for a non published dataset"):
            records_upsert = RecordsBulkUpsert(
                items=[
                    RecordUpsert(fields={"text": "hello world"}, metadata={"source": "test"}),
                ]
            )
            RecordsBulkUpsertValidator(records_upsert, db).validate_for(dataset)

    async def test_records_bulk_upsert_validator_with_record_error(self, db: AsyncSession):
        dataset = await self.configure_dataset()
        records_upsert = RecordsBulkUpsert(
            items=[
                RecordUpsert(fields={"text": "hello world"}, metadata={"source": "test"}),
                RecordUpsert(fields={"text": "hello world"}, metadata={"source": "test"}),
                RecordUpsert(fields={"wrong-field": "hello world"}),
            ]
        )

        with pytest.raises(
            ValueError,
            match="record at position 2 is not valid because",
        ):
            RecordsBulkUpsertValidator(records_upsert, db).validate_for(dataset)
