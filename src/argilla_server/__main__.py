#  coding=utf-8
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
import warnings

if __name__ == "__main__":
    import uvicorn

    warnings.warn(
        "\n'python -m argilla_server' command is deprecated and will be removed in the next major release. "
        "\nPlease use 'python -m argilla' instead",
        category=FutureWarning,
    )

    uvicorn.run(
        "argilla_server:app",
        port=6900,
        host="0.0.0.0",
        access_log=True,
    )
