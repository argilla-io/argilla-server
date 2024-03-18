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

from typing import Annotated, Optional

from argilla_server.pydantic_v1 import Field

SUGGESTION_SCORE_GREATER_THAN_OR_EQUAL = 0
SUGGESTION_SCORE_LESS_THAN_OR_EQUAL = 1

# TODO: This field has been defined here because it's used by models questions file (aka check_responses) and to
# avoid cyclical import errors. Once that we remove check_responses functionality we can move this field
# again to be used in the necessary schema model.
SuggestionScoreField = Annotated[
    Optional[float],
    Field(
        ge=SUGGESTION_SCORE_GREATER_THAN_OR_EQUAL,
        le=SUGGESTION_SCORE_LESS_THAN_OR_EQUAL,
        description="The score assigned to the suggestion",
    ),
]
