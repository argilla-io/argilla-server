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

from typing import Any, Dict, Generic, List, Literal, Optional, Protocol, TypeVar, Union

from argilla_server.enums import QuestionType, ResponseStatus
from argilla_server.pydantic_v1 import BaseModel, Field, root_validator
from argilla_server.schemas.v1.commons.suggestions import SuggestionScoreField

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


SPAN_QUESTION_RESPONSE_VALUE_MAX_ITEMS = 10_000


class ResponseValue(Protocol):
    value: Any


class BaseQuestionSettings(BaseModel):
    # TODO: We can't import Record because it can cause a cyclical import error.
    # We should move this functionality outside models package to avoid this.
    def check_response(self, response: ResponseValue, record: "Record", status: Optional[ResponseStatus] = None):
        pass


class TextQuestionSettings(BaseQuestionSettings):
    type: Literal[QuestionType.text]
    use_markdown: bool = False

    def check_response(self, response: ResponseValue, record: "Record", status: Optional[ResponseStatus] = None):
        if not isinstance(response.value, str):
            raise ValueError(f"Expected text value, found {type(response.value)}")


class RatingQuestionSettingsOption(BaseModel):
    value: int


T = TypeVar("T")


class ValidOptionCheckerMixin(BaseQuestionSettings, Generic[T]):
    @property
    def option_values(self) -> List[T]:
        return [option.value for option in self.options]

    def check_response(self, response: ResponseValue, record: "Record", status: Optional[ResponseStatus] = None):
        if response.value not in self.option_values:
            raise ValueError(f"{response.value!r} is not a valid option.\nValid options are: {self.option_values!r}")


class RatingQuestionSettings(ValidOptionCheckerMixin[int]):
    type: Literal[QuestionType.rating]
    options: List[RatingQuestionSettingsOption]


class ValueTextQuestionSettingsOption(BaseModel):
    value: str
    text: str
    description: Optional[str] = None


class LabelSelectionQuestionSettings(ValidOptionCheckerMixin[str]):
    type: Literal[QuestionType.label_selection]
    options: List[ValueTextQuestionSettingsOption]
    visible_options: Optional[int] = None


def _are_all_elements_in_list(elements: List[T], list_: List[T]) -> List[T]:
    return sorted(list(set(elements) - set(list_)))


class MultiLabelSelectionQuestionSettings(LabelSelectionQuestionSettings):
    type: Literal[QuestionType.multi_label_selection]

    def check_response(self, response: ResponseValue, record: "Record", status: Optional[ResponseStatus] = None):
        if not isinstance(response.value, list):
            raise ValueError(
                f"This MultiLabelSelection question expects a list of values, found {type(response.value)}"
            )

        if len(response.value) == 0:
            raise ValueError("This MultiLabelSelection question expects a list of values, found empty list")

        unique_values = set(response.value)
        if len(unique_values) != len(response.value):
            raise ValueError(
                "This MultiLabelSelection question expects a list of unique values, but duplicates were found"
            )

        invalid_options = _are_all_elements_in_list(response.value, self.option_values)
        if invalid_options:
            raise ValueError(
                f"{invalid_options!r} are not valid options for this MultiLabelSelection question.\nValid options are:"
                f" {self.option_values!r}"
            )


class RankingQuestionSettings(ValidOptionCheckerMixin[str]):
    type: Literal[QuestionType.ranking]
    options: List[ValueTextQuestionSettingsOption]

    @property
    def rank_values(self) -> List[int]:
        return list(range(1, len(self.option_values) + 1))

    def check_response(self, response: ResponseValue, record: "Record", status: Optional[ResponseStatus] = None):
        if not isinstance(response.value, list):
            raise ValueError(f"This Ranking question expects a list of values, found {type(response.value)}")

        values = []
        ranks = []
        for response_option in response.value:
            values.append(response_option.get("value"))
            ranks.append(response_option.get("rank"))

        # Only if the response is submitted check that all the possible options have been ranked or that all the
        # provided options contains a valid rank
        if status == ResponseStatus.submitted:
            if len(response.value) != len(self.option_values):
                raise ValueError(
                    f"This Ranking question expects a list containing {len(self.option_values)} values, found a list of"
                    f" {len(response.value)} values"
                )

            invalid_ranks = _are_all_elements_in_list(ranks, self.rank_values)
            if invalid_ranks:
                raise ValueError(
                    f"{invalid_ranks!r} are not valid ranks for this Ranking question.\nValid ranks are:"
                    f" {self.rank_values!r}"
                )

        invalid_values = _are_all_elements_in_list(values, self.option_values)
        if invalid_values:
            raise ValueError(
                f"{invalid_values!r} are not valid options for this Ranking question.\nValid options are:"
                f" {self.option_values!r}"
            )

        unique_values = set(values)
        if len(response.value) != len(unique_values):
            raise ValueError("This Ranking question expects a list of unique values, but duplicates were found")


class SpanQuestionResponseValueItem(BaseModel):
    label: str
    start: int = Field(..., ge=0)
    end: int = Field(..., ge=1)
    # NOTE: score field it's only used for suggestions and not for responses, right now we don't have a
    # way to differentiate between the two so we are defining it here to validate suggestions where the field
    # it's available.
    score: SuggestionScoreField

    @root_validator(skip_on_failure=True)
    def check_start_and_end(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        start, end = values.get("start"), values.get("end")

        if start is not None and end is not None and end <= start:
            raise ValueError("span question response value 'end' must have a value greater than 'start'")

        return values


class SpanQuestionResponseValue(BaseModel):
    value: List[SpanQuestionResponseValueItem] = Field(..., max_items=SPAN_QUESTION_RESPONSE_VALUE_MAX_ITEMS)


class SpanQuestionSettings(BaseQuestionSettings):
    type: Literal[QuestionType.span]
    field: str
    options: List[ValueTextQuestionSettingsOption]

    def check_response(self, response: ResponseValue, record: "Record", status: Optional[ResponseStatus] = None):
        if not isinstance(response.value, list):
            raise ValueError(f"span question expects a list of values, found {type(response.value)}")

        if self.field not in record.fields:
            raise ValueError(f"span question requires record to have field `{self.field}`")

        span_question_response_value = self._parse_response_value(response)
        self._check_response_start_end_ranges(span_question_response_value, len(record.fields[self.field]))
        self._check_response_labels(span_question_response_value)

    def _parse_response_value(self, response_value: ResponseValue) -> SpanQuestionResponseValue:
        return SpanQuestionResponseValue.parse_obj(response_value)

    def _check_response_start_end_ranges(self, span_question_response_value: SpanQuestionResponseValue, field_len: int):
        for value_item in span_question_response_value.value:
            if value_item.start > (field_len - 1):
                raise ValueError(
                    f"span question response value `start` must have a value lower than record field `{self.field}` length that is `{field_len}`"
                )

            if value_item.end > field_len:
                raise ValueError(
                    f"span question response value `end` must have a value lower or equal than record field `{self.field}` length that is `{field_len}`"
                )

    def _check_response_labels(self, span_question_response_value: SpanQuestionResponseValue):
        labels = [option.value for option in self.options]

        for value_item in span_question_response_value.value:
            if not value_item.label in labels:
                raise ValueError(
                    f"undefined label '{value_item.label}' for span question.\nValid labels are: {labels!r}"
                )


QuestionSettings = Annotated[
    Union[
        TextQuestionSettings,
        RatingQuestionSettings,
        LabelSelectionQuestionSettings,
        MultiLabelSelectionQuestionSettings,
        RankingQuestionSettings,
        SpanQuestionSettings,
    ],
    Field(..., discriminator="type"),
]
