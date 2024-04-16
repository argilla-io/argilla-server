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

"""change suggestions score column to json

Revision ID: ca7293c38970
Revises: bda6fe24314e
Create Date: 2024-04-08 13:14:48.437677

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ca7293c38970"
down_revision = "bda6fe24314e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("suggestions") as batch_op:
        batch_op.alter_column("score", type_=sa.JSON(), postgresql_using="to_json(score)")


def downgrade() -> None:
    # TODO: We should check what to do here.
    pass
