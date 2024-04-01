from typing import List

from argilla_server.models import VectorSettings


class VectorValidator:
    def __init__(self, value: List[float]):
        self._value = value

    def validate_for(self, vector_settings: VectorSettings):
        if len(self._value) != vector_settings.dimensions:
            raise ValueError(f"vector must have {vector_settings.dimensions} elements, got {len(self._value)} elements")
