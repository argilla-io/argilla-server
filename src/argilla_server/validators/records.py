import copy
from abc import ABC, abstractmethod
from typing import Union, Dict

from argilla_server.models import Dataset
from argilla_server.schemas.v1.records import RecordCreate, RecordUpdate


class RecordValidatorBase(ABC):
    def __init__(self, record_change: Union[RecordCreate, RecordUpdate]):
        self._record_change = record_change

    @abstractmethod
    def validate_for(self, dataset: Dataset) -> None:
        pass

    def _validate_fields(self, dataset: Dataset) -> None:
        fields = self._record_change.fields or {}

        self._validate_required_fields(dataset, fields)
        self._validate_extra_fields(dataset, fields)

    def _validate_metadata(self, dataset: Dataset) -> None:
        metadata = self._record_change.metadata or {}
        for name, value in metadata.items():
            metadata_property = dataset.metadata_property_by_name(name)
            # TODO(@frascuchon): Create a MetadataPropertyValidator instead of using the parsed_settings
            if metadata_property and value is not None:
                try:
                    metadata_property.parsed_settings.check_metadata(value)
                except ValueError as e:
                    raise ValueError(
                        f"metadata is not valid: '{name}' metadata property validation failed because {e}"
                    ) from e

            elif metadata_property is None and not dataset.allow_extra_metadata:
                raise ValueError(
                    f"metadata is not valid: '{name}' metadata property does not exists for dataset '{dataset.id}' "
                    "and extra metadata is not allowed for this dataset"
                )

    def _validate_required_fields(self, dataset: Dataset, fields: Dict[str, str]) -> None:
        for field in dataset.fields:
            if field.required and not (field.name in fields and fields.get(field.name) is not None):
                raise ValueError(f"missing required value for field: {field.name!r}")

    def _validate_extra_fields(self, dataset: Dataset, fields: Dict[str, str]) -> None:
        fields_copy = copy.copy(fields)
        for field in dataset.fields:
            fields_copy.pop(field.name, None)
        if fields_copy:
            raise ValueError(f"found fields values for non configured fields: {list(fields_copy.keys())}")


class RecordCreateValidator(RecordValidatorBase):
    def __init__(self, record_create: RecordCreate):
        super().__init__(record_create)

    def validate_for(self, dataset: Dataset) -> None:
        self._validate_fields(dataset)
        self._validate_metadata(dataset)


class RecordUpdateValidator(RecordValidatorBase):
    def __init__(self, record_upsert: RecordUpdate):
        super().__init__(record_upsert)

    def validate_for(self, dataset: Dataset) -> None:
        self._validate_metadata(dataset)
