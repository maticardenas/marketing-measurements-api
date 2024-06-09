from typing import Any

from ninja import Schema
from ninja.pagination import PaginationBase
from pydantic import Field


class MarketingDataPagination(PaginationBase):
    class Input(Schema):
        offset: int = Field(0, ge=0)
        page_size: int = Field(10, gt=0, le=100)

    class Output(Schema):
        data: list[Any]

    items_attribute: str = "data"

    def paginate_queryset(self, queryset, pagination: Input, **params):
        return {
            "data": queryset[
                pagination.offset : pagination.offset + pagination.page_size
            ],
        }
