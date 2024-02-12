from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from argilla_server.apis.v1.handlers.datasets.datasets import _get_dataset_or_raise
from argilla_server.contexts import datasets
from argilla_server.database import get_async_db
from argilla_server.models import User
from argilla_server.policies import DatasetPolicyV1, authorize
from argilla_server.schemas.v1.questions import Question, QuestionCreate, Questions
from argilla_server.security import auth

router = APIRouter()


@router.get("/datasets/{dataset_id}/questions", response_model=Questions)
async def list_dataset_questions(
    *, db: AsyncSession = Depends(get_async_db), dataset_id: UUID, current_user: User = Security(auth.get_current_user)
):
    dataset = await _get_dataset_or_raise(db, dataset_id, with_questions=True)

    await authorize(current_user, DatasetPolicyV1.get(dataset))

    return Questions(items=dataset.questions)


@router.post("/datasets/{dataset_id}/questions", status_code=status.HTTP_201_CREATED, response_model=Question)
async def create_dataset_question(
    *,
    db: AsyncSession = Depends(get_async_db),
    dataset_id: UUID,
    question_create: QuestionCreate,
    current_user: User = Security(auth.get_current_user),
):
    dataset = await _get_dataset_or_raise(db, dataset_id)

    await authorize(current_user, DatasetPolicyV1.create_question(dataset))

    if await datasets.get_question_by_name_and_dataset_id(db, question_create.name, dataset_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Question with name `{question_create.name}` already exists for dataset with id `{dataset_id}`",
        )

    # TODO: We should split API v1 into different FastAPI apps so we can customize error management.
    # After mapping ValueError to 422 errors for API v1 then we can remove this try except.
    try:
        return await datasets.create_question(db, dataset, question_create)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(err))
