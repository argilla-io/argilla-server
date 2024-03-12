from argilla_server.enums import QuestionType, ResponseStatus
from argilla_server.schemas.v1.questions import SpanQuestionSettings, RatingQuestionSettings, LabelSelectionQuestionSettings, MultiLabelSelectionQuestionSettings, RankingQuestionSettings
from argilla_server.schemas.v1.responses import RatingQuestionResponseValue, ResponseCreate, ResponseValueCreate, ResponseValuesCreate, RankingQuestionResponseValue, SpanQuestionResponseValue, TextAndLabelSelectionQuestionResponseValue, MultiLabelSelectionQuestionResponseValue
from argilla_server.models import Record, Question


class ResponseCreateValidator:
    def __init__(self, response_create: ResponseCreate) -> None:
        self._response_create = response_create

    def validate_for(self, record: Record) -> None:
        self._validate_values_are_present_when_submitted()
        self._validate_required_questions_have_values(record)
        self._validate_values_have_configured_questions(record)
        self._validate_values(record)

    def _validate_values_are_present_when_submitted(self) -> None:
        if self._response_create.is_submitted and not self._response_create.values:
            raise ValueError("missing response values for submitted response")

    def _validate_required_questions_have_values(self, record: Record) -> None:
        for question in record.dataset.questions:
            if self._response_create.is_submitted and question.required and question.name not in self._response_create.values:
                raise ValueError(f"missing response value for required question with name={question.name}")

    def _validate_values_have_configured_questions(self, record: Record) -> None:
        question_names = [question.name for question in record.dataset.questions]

        for value_question_name in self._response_create.values or []:
            if value_question_name not in question_names:
                raise ValueError(f"found response value for non configured question with name={value_question_name!r}")

    def _validate_values(self, record: Record) -> None:
        if not self._response_create.values:
            return

        for question in record.dataset.questions:
            if question_response := self._response_create.values.get(question.name):
                if question.type == QuestionType.text:
                    TextQuestionResponseValueValidator(question_response.value).validate()
                elif question.type == QuestionType.label_selection:
                    LabelSelectionQuestionResponseValueValidator(question_response.value).validate_for(question.parsed_settings)
                elif question.type == QuestionType.multi_label_selection:
                    MultiLabelSelectionQuestionResponseValueValidator(question_response.value).validate_for(question.parsed_settings)
                elif question.type == QuestionType.rating:
                    RatingQuestionResponseValueValidator(question_response.value).validate_for(question.parsed_settings)
                elif question.type == QuestionType.ranking:
                    RankingQuestionResponseValueValidator(question_response.value).validate_for(self._response_create.status, question.parsed_settings)
                elif question.type == QuestionType.span:
                    SpanQuestionResponseValueValidator(question_response.value).validate_for(question.parsed_settings, record)
                else:
                    raise ValueError(f"unknown question type f{question.type!r} for question with name f{question.name}")


class TextQuestionResponseValueValidator:
    def __init__(self, response_value: TextAndLabelSelectionQuestionResponseValue):
        self._response_value = response_value

    def validate(self) -> None:
        self._validate_value_type()

    def _validate_value_type(self) -> None:
        if not isinstance(self._response_value, str):
            raise ValueError(f"text question expects a text value, found {type(self._response_value)}")


class LabelSelectionQuestionResponseValueValidator:
    def __init__(self, response_value: TextAndLabelSelectionQuestionResponseValue):
        self._response_value = response_value

    def validate_for(self, label_selection_question_settings: LabelSelectionQuestionSettings) -> None:
        self._validate_label_is_available_at_question_settings(label_selection_question_settings)

    def _validate_label_is_available_at_question_settings(self, label_selection_question_settings: LabelSelectionQuestionSettings) -> None:
        available_labels = [option.value for option in label_selection_question_settings.options]

        if self._response_value not in available_labels:
            raise ValueError(f"{self._response_value!r} is not a valid label for label selection question.\nValid labels are: {available_labels!r}")


class MultiLabelSelectionQuestionResponseValueValidator:
    def __init__(self, response_value: MultiLabelSelectionQuestionResponseValue):
        self._response_value = response_value

    def validate_for(self, multi_label_selection_question_settings: MultiLabelSelectionQuestionSettings) -> None:
        self._validate_value_type()
        self._validate_labels_are_not_empty()
        self._validate_labels_are_unique()
        self._validate_labels_are_available_at_question_settings(multi_label_selection_question_settings)

    def _validate_value_type(self) -> None:
        if not isinstance(self._response_value, list):
            raise ValueError(f"multi label selection questions expects a list of values, found {type(self._response_value)}")

    def _validate_labels_are_not_empty(self) -> None:
        if len(self._response_value) == 0:
            raise ValueError("multi label selection questions expects a list of values, found empty list")

    def _validate_labels_are_unique(self) -> None:
        if len(self._response_value) != len(set(self._response_value)):
            raise ValueError("multi label selection questions expect a list of unique values, but duplicates were found")

    def _validate_labels_are_available_at_question_settings(self, multi_label_selection_question_settings: MultiLabelSelectionQuestionSettings) -> None:
        available_labels = [option.value for option in multi_label_selection_question_settings.options]
        invalid_labels = sorted(list(set(self._response_value) - set(available_labels)))

        if invalid_labels:
            raise ValueError(f"{invalid_labels!r} are not valid labels for multi label selection question.\nValid labels are: {available_labels!r}")


class RatingQuestionResponseValueValidator:
    def __init__(self, response_value: RatingQuestionResponseValue):
        self._response_value = response_value

    def validate_for(self, rating_question_settings: RatingQuestionSettings) -> None:
        self._validate_rating_is_available_at_question_settings(rating_question_settings)

    def _validate_rating_is_available_at_question_settings(self, rating_question_settings: RatingQuestionSettings) -> None:
        available_options = [option.value for option in rating_question_settings.options]

        if self._response_value not in available_options:
            raise ValueError(f"{self._response_value!r} is not a valid rating for rating question.\nValid ratings are: {available_options!r}")


class RankingQuestionResponseValueValidator:
    def __init__(self, response_value: RankingQuestionResponseValue):
        self._response_value = response_value

    def validate_for(self, response_status: ResponseStatus, ranking_question_settings: RankingQuestionSettings) -> None:
        self._validate_value_type()
        self._validate_all_rankings_are_present_when_submitted(response_status, ranking_question_settings)
        self._validate_all_rankings_are_valid_when_submitted(response_status, ranking_question_settings)
        self._validate_values_are_available_at_question_settings(ranking_question_settings)
        self._validate_values_are_unique()

    def _validate_value_type(self) -> None:
        if not isinstance(self._response_value, list):
            raise ValueError(f"ranking question expects a list of values, found {type(self._response_value)}")

    def _validate_all_rankings_are_present_when_submitted(self, response_status: ResponseStatus, ranking_question_settings: RankingQuestionSettings) -> None:
        if response_status != ResponseStatus.submitted:
            return

        available_values = [option.value for option in ranking_question_settings.options]
        available_values_len = len(available_values)

        if len(self._response_value) != available_values_len:
            raise ValueError(f"ranking question expects a list containing {available_values_len} values, found a list of {len(self._response_value)} values")

    def _validate_all_rankings_are_valid_when_submitted(self, response_status: ResponseStatus, ranking_question_settings: RankingQuestionSettings) -> None:
        if response_status != ResponseStatus.submitted:
            return

        available_rankings = list(range(1, len(ranking_question_settings.options) + 1))
        response_rankings = [value_item.rank for value_item in self._response_value]
        invalid_rankings = sorted(list(set(response_rankings) - set(available_rankings)))

        if invalid_rankings:
            raise ValueError(f"{invalid_rankings!r} are not valid ranks for ranking question.\nValid ranks are: {available_rankings!r}")

    def _validate_values_are_available_at_question_settings(self, ranking_question_settings: RankingQuestionSettings) -> None:
        available_values = [option.value for option in ranking_question_settings.options]
        response_values = [value_item.value for value_item in self._response_value]
        invalid_values = sorted(list(set(response_values) - set(available_values)))

        if invalid_values:
            raise ValueError(f"{invalid_values!r} are not valid values for ranking question.\nValid values are: {available_values!r}")

    def _validate_values_are_unique(self) -> None:
        response_values = [value_item.value for value_item in self._response_value]

        if len(response_values) != len(set(response_values)):
            raise ValueError("ranking question expects a list of unique values, but duplicates were found")


class SpanQuestionResponseValueValidator:
    def __init__(self, response_value: SpanQuestionResponseValue):
        self._response_value = response_value

    def validate_for(self, span_question_settings: SpanQuestionSettings, record: Record) -> None:
        self._validate_value_type()
        self._validate_question_settings_field_is_present_at_record(span_question_settings, record)
        self._validate_start_end_are_within_record_field_limits(span_question_settings, record)
        self._validate_labels_are_available_at_question_settings(span_question_settings)

    def _validate_value_type(self) -> None:
        if not isinstance(self._response_value, list):
            raise ValueError(f"span question expects a list of values, found {type(self._response_value)}")

    def _validate_question_settings_field_is_present_at_record(self, span_question_settings: SpanQuestionSettings, record: Record) -> None:
        if span_question_settings.field not in record.fields:
            raise ValueError(f"span question requires record to have field `{span_question_settings.field}`")

    def _validate_start_end_are_within_record_field_limits(self, span_question_settings: SpanQuestionSettings, record: Record) -> None:
        field_len = len(record.fields[span_question_settings.field])

        for value_item in self._response_value:
            if value_item.start > (field_len - 1):
                raise ValueError(f"span question response value `start` must have a value lower than record field `{span_question_settings.field}` length that is `{field_len}`")

            if value_item.end > field_len:
                raise ValueError(f"span question response value `end` must have a value lower or equal than record field `{span_question_settings.field}` length that is `{field_len}`")

    def _validate_labels_are_available_at_question_settings(self, span_question_settings: SpanQuestionSettings) -> None:
        available_labels = [option.value for option in span_question_settings.options]

        for value_item in self._response_value:
            if not value_item.label in available_labels:
                raise ValueError(f"undefined label '{value_item.label}' for span question.\nValid labels are: {available_labels!r}")
