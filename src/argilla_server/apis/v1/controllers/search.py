from typing import Annotated, Union, Literal, List, Optional
from uuid import UUID

from fastapi import APIRouter

from argilla_server.pydantic_v1 import BaseModel, Field
from argilla_server.schemas.v1.records import FilterScope

router = APIRouter(tags=["search"])


class FilterBase(BaseModel):
    type: str
    scope: FilterScope


class EqualsFilter(FilterBase):
    type: Literal["eq"]
    value: str


class InFilter(FilterBase):
    type: Literal["in"]
    values: List[str]


class GreaterThanFilter(FilterBase):
    type: Literal["gt"]
    value: str


class LessThanFilter(FilterBase):
    type: Literal["lt"]
    value: str


class GreaterThanOrEqualFilter(FilterBase):
    type: Literal["gte"]
    value: str


class LessThanOrEqualFilter(FilterBase):
    type: Literal["lte"]
    value: str


class TextQueryFilter(FilterBase):
    type: Literal["text_query"]
    query: str
    scope: Optional[FilterScope]


class TermsFilter(FilterBase):
    type: Literal["terms"]
    terms: List[str]


class RangeFilter(FilterBase):
    type: Literal["range"]
    gte: str
    lte: str


class AndFilter(BaseModel):
    type: Literal["and"]
    filters: List["Filter"]


class OrFilter(BaseModel):
    type: Literal["or"]
    filters: List["Filter"]


class NotFilter(BaseModel):
    type: Literal["not"]
    filter: "Filter"


Filter = Annotated[
    Union[
        AndFilter,
        OrFilter,
        NotFilter,
        InFilter,
        RangeFilter,
        TermsFilter,
        TextQueryFilter,
        EqualsFilter,
        GreaterThanFilter,
        GreaterThanOrEqualFilter,
        LessThanFilter,
        LessThanOrEqualFilter,
    ],
    Field(..., discriminator="type"),
]


AndFilter.update_forward_refs()
OrFilter.update_forward_refs()
NotFilter.update_forward_refs()


class Sort(BaseModel):
    field: str
    order: Literal["asc", "desc"]


class RecordsSearchQuery(BaseModel):
    filter: Filter
    sort: Optional[List[Sort]]


class RecordsSearchResponse(BaseModel):
    query: RecordsSearchQuery


@router.post("/search/records", response_model=RecordsSearchResponse)
async def search(
    *,
    dataset_id: UUID,
    search_query: RecordsSearchQuery,
):

    return RecordsSearchResponse(query=search_query)
