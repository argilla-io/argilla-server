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

import copy
from abc import ABC
from typing import Dict, Union, overload

from argilla_server.models import Dataset, Record
from argilla_server.schemas.v1.records import RecordCreate, RecordUpdate, RecordUpsert


class RecordValidatorBase(ABC):
    def __init__(self, record_change: Union[RecordCreate, RecordUpdate, RecordUpsert]):
        self._record_change = record_change

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
    def __init__(self, record_update: RecordUpdate):
        super().__init__(record_update)

    def validate_for(self, record: Record) -> None:
        self._validate_metadata(record.dataset)
        self._validate_duplicated_suggestions()

    def _validate_duplicated_suggestions(self):
        if not self._record_change.suggestions:
            return
        # TODO: This validation should be defined as pydantic model validation
        #  We keep it here to maintain the generated error message.
        question_ids = [s.question_id for s in self._record_change.suggestions]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("found duplicate suggestions question IDs")


class RecordUpsertValidator(RecordValidatorBase):
    def __init__(self, record_upsert: RecordUpsert):
        super().__init__(record_upsert)

    @overload
    def validate_for(self, dataset: Dataset) -> None: ...
    @overload
    def validate_for(self, record: Record) -> None: ...

    def validate_for(self, model: Union[Dataset, Record]) -> None:
        if isinstance(model, Dataset):
            self._validate_fields(model)
            self._validate_metadata(model)
        else:
            self._validate_metadata(model.dataset)
