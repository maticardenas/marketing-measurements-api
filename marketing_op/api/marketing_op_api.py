from django.http import HttpRequest
from ninja import NinjaAPI, Router, Query
from ninja.pagination import paginate

from api.pagination import MarketingDataPagination
from api.schemas import (
    MarketingDataSchema,
    MarketingDataFilterSchema,
    ChannelSalesPercentageSchema,
)
from api.services.marketing_measurements import get_marketing_data
from api.services.marketing_stats import get_channel_sales_percentages

api = NinjaAPI()

router = Router()


@router.get(
    "/measurements/",
    response={200: list[MarketingDataSchema]},
)
@paginate(MarketingDataPagination)
def marketing_measurements(
    request: HttpRequest, filters: MarketingDataFilterSchema = Query(None)
):
    data = get_marketing_data(filters.dict() if filters else {})
    return data


@router.get(
    "/stats/channel-sales-percentages/",
    response={200: list[ChannelSalesPercentageSchema]},
)
@paginate(MarketingDataPagination)
def channel_sales_percentages(
    request: HttpRequest, filters: MarketingDataFilterSchema = Query(None)
):
    data = get_channel_sales_percentages(filters.dict() if filters else {})
    return data


api.add_router("/marketing", router)
