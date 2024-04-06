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

from typing import Dict, List, Optional, Tuple
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from argilla_server.apis.v1.handlers.datasets.datasets import _get_dataset_or_raise
from argilla_server.apis.v1.handlers.datasets.records_search import (
    LIST_DATASET_RECORDS_DEFAULT_SORT_BY,
    LIST_DATASET_RECORDS_LIMIT_DEFAULT,
    LIST_DATASET_RECORDS_LIMIT_LE,
    SortByQueryParamParsed,
    _get_search_responses,
    parse_record_include_param,
)
from argilla_server.contexts import datasets
from argilla_server.contexts.bulk.records.records_create_bulk import RecordsCreateBulk
from argilla_server.contexts.bulk.records.records_update_bulk import RecordsUpdateBulk
from argilla_server.contexts.bulk.records.records_upsert_bulk import RecordsUpsertBulk
from argilla_server.database import get_async_db
from argilla_server.enums import ResponseStatusFilter
from argilla_server.models import User
from argilla_server.policies import DatasetPolicyV1, authorize
from argilla_server.schemas.v1.datasets import Dataset
from argilla_server.schemas.v1.records import (
    MetadataParsedQueryParam,
    MetadataQueryParams,
    Record,
    RecordIncludeParam,
    Records,
    RecordsBulk,
    RecordsCreate,
    RecordsUpdate,
    RecordsBulkCreate,
)
from argilla_server.search_engine import (
    SearchEngine,
    get_search_engine,
)
from argilla_server.security import auth
from argilla_server.telemetry import TelemetryClient, get_telemetry_client
from argilla_server.utils import parse_uuids

DELETE_DATASET_RECORDS_LIMIT = 100

router = APIRouter()


@router.get("/me/datasets/{dataset_id}/records", response_model=Records, response_model_exclude_unset=True)
async def list_current_user_dataset_records(
    *,
    db: AsyncSession = Depends(get_async_db),
    search_engine: SearchEngine = Depends(get_search_engine),
    dataset_id: UUID,
    metadata: MetadataQueryParams = Depends(),
    sort_by_query_param: SortByQueryParamParsed,
    include: Optional[RecordIncludeParam] = Depends(parse_record_include_param),
    response_statuses: List[ResponseStatusFilter] = Query([], alias="response_status"),
    offset: int = 0,
    limit: int = Query(default=LIST_DATASET_RECORDS_LIMIT_DEFAULT, ge=1, le=LIST_DATASET_RECORDS_LIMIT_LE),
    current_user: User = Security(auth.get_current_user),
):
    dataset = await _get_dataset_or_raise(db, dataset_id)

    await authorize(current_user, DatasetPolicyV1.get(dataset))

    records, total = await _filter_records_using_search_engine(
        db,
        search_engine,
        dataset=dataset,
        parsed_metadata=metadata.metadata_parsed,
        limit=limit,
        offset=offset,
        user=current_user,
        response_statuses=response_statuses,
        include=include,
        sort_by_query_param=sort_by_query_param,
    )

    return Records(items=records, total=total)


@router.get("/datasets/{dataset_id}/records", response_model=Records, response_model_exclude_unset=True)
async def list_dataset_records(
    *,
    db: AsyncSession = Depends(get_async_db),
    search_engine: SearchEngine = Depends(get_search_engine),
    dataset_id: UUID,
    metadata: MetadataQueryParams = Depends(),
    sort_by_query_param: SortByQueryParamParsed,
    include: Optional[RecordIncludeParam] = Depends(parse_record_include_param),
    response_statuses: List[ResponseStatusFilter] = Query([], alias="response_status"),
    offset: int = 0,
    limit: int = Query(default=LIST_DATASET_RECORDS_LIMIT_DEFAULT, ge=1, le=LIST_DATASET_RECORDS_LIMIT_LE),
    current_user: User = Security(auth.get_current_user),
):
    dataset = await _get_dataset_or_raise(db, dataset_id)

    await authorize(current_user, DatasetPolicyV1.list_records_with_all_responses(dataset))

    records, total = await _filter_records_using_search_engine(
        db,
        search_engine,
        dataset=dataset,
        parsed_metadata=metadata.metadata_parsed,
        limit=limit,
        offset=offset,
        response_statuses=response_statuses,
        include=include,
        sort_by_query_param=sort_by_query_param or LIST_DATASET_RECORDS_DEFAULT_SORT_BY,
    )

    return Records(items=records, total=total)


@router.post("/datasets/{dataset_id}/records", status_code=status.HTTP_204_NO_CONTENT)
async def create_dataset_records(
    *,
    db: AsyncSession = Depends(get_async_db),
    search_engine: SearchEngine = Depends(get_search_engine),
    telemetry_client: TelemetryClient = Depends(get_telemetry_client),
    dataset_id: UUID,
    records_create: RecordsCreate,
    current_user: User = Security(auth.get_current_user),
):
    dataset = await _get_dataset_or_raise(
        db, dataset_id, with_fields=True, with_questions=True, with_metadata_properties=True, with_vectors_settings=True
    )

    await authorize(current_user, DatasetPolicyV1.create_records(dataset))

    # TODO: We should split API v1 into different FastAPI apps so we can customize error management.
    #  After mapping ValueError to 422 errors for API v1 then we can remove this try except.
    try:
        await RecordsCreateBulk(db, search_engine).create_dataset_records(dataset, records_create)
        telemetry_client.track_data(action="DatasetRecordsCreated", data={"records": len(records_create.items)})
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(err))


@router.patch("/datasets/{dataset_id}/records", status_code=status.HTTP_204_NO_CONTENT)
async def update_dataset_records(
    *,
    db: AsyncSession = Depends(get_async_db),
    search_engine: SearchEngine = Depends(get_search_engine),
    telemetry_client: TelemetryClient = Depends(get_telemetry_client),
    dataset_id: UUID,
    records_update: RecordsUpdate,
    current_user: User = Security(auth.get_current_user),
):
    dataset = await _get_dataset_or_raise(
        db,
        dataset_id,
        with_fields=True,
        with_questions=True,
        with_metadata_properties=True,
        with_vectors_settings=True,
    )

    await authorize(current_user, DatasetPolicyV1.update_records(dataset))

    try:
        await RecordsUpdateBulk(db, search_engine).update_dataset_records(dataset, records_update)
        telemetry_client.track_data(action="DatasetRecordsUpdated", data={"records": len(records_update.items)})
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(err))


@router.post(
    "/datasets/{dataset_id}/records/bulk",
    response_model=RecordsBulk,
    status_code=status.HTTP_200_OK,
    response_model_exclude_unset=True,
)
async def create_bulk_dataset_records(
    *,
    dataset_id: UUID,
    records_upsert: RecordsBulkCreate,
    db: AsyncSession = Depends(get_async_db),
    search_engine: SearchEngine = Depends(get_search_engine),
    current_user: User = Security(auth.get_current_user),
):
    dataset = await _get_dataset_or_raise(
        db,
        dataset_id,
        with_fields=True,
        with_questions=True,
        with_metadata_properties=True,
        with_vectors_settings=True,
    )

    await authorize(current_user, DatasetPolicyV1.create_records(dataset))

    records = await RecordsUpsertBulk(db, search_engine).upsert_dataset_records(dataset, records_upsert)
    return RecordsBulk(items=records)


@router.delete("/datasets/{dataset_id}/records", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset_records(
    *,
    db: AsyncSession = Depends(get_async_db),
    search_engine: SearchEngine = Depends(get_search_engine),
    dataset_id: UUID,
    current_user: User = Security(auth.get_current_user),
    ids: str = Query(..., description="A comma separated list with the IDs of the records to be removed"),
):
    dataset = await _get_dataset_or_raise(db, dataset_id)

    await authorize(current_user, DatasetPolicyV1.delete_records(dataset))

    record_ids = parse_uuids(ids)
    num_records = len(record_ids)

    if num_records == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No record IDs provided")

    if num_records > DELETE_DATASET_RECORDS_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Cannot delete more than {DELETE_DATASET_RECORDS_LIMIT} records at once",
        )

    await datasets.delete_records(db, search_engine, dataset, record_ids)


async def _filter_records_using_search_engine(
    db: "AsyncSession",
    search_engine: "SearchEngine",
    dataset: Dataset,
    parsed_metadata: List[MetadataParsedQueryParam],
    limit: int,
    offset: int,
    user: Optional[User] = None,
    response_statuses: Optional[List[ResponseStatusFilter]] = None,
    include: Optional[RecordIncludeParam] = None,
    sort_by_query_param: Optional[Dict[str, str]] = None,
) -> Tuple[List["Record"], int]:
    search_responses = await _get_search_responses(
        db=db,
        search_engine=search_engine,
        dataset=dataset,
        limit=limit,
        offset=offset,
        user=user,
        parsed_metadata=parsed_metadata,
        response_statuses=response_statuses,
        sort_by_query_param=sort_by_query_param,
    )

    record_ids = [response.record_id for response in search_responses.items]
    user_id = user.id if user else None

    return (
        await datasets.get_records_by_ids(
            db=db,
            dataset_id=dataset.id,
            user_id=user_id,
            records_ids=record_ids,
            include=include,
        ),
        search_responses.total,
    )
