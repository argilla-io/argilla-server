from argilla_server.enums import ResponseStatus
from argilla_server.schemas.v1.responses import ResponseCreate, ResponseValuesCreate
from argilla_server.models import Record


class ResponseCreateValidator:
    def __init__(self, response_create: ResponseCreate) -> None:
        self._response_create = response_create

    def validate_for(self, record: Record) -> None:
        self._validate_values_are_present_when_submitted()
        self._validate_required_questions_have_values(record)
        self._validate_values_have_configured_questions(record)
        self._validate_values(record)

    def _validate_values_are_present_when_submitted(self):
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
                question.parsed_settings.check_response(question_response, record, self._response_create.status)
