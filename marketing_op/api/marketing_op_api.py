from django.http import HttpRequest
from ninja import NinjaAPI, Router, Query
from ninja.pagination import paginate

from api.security import BasicAuth, AuthBearer
from api.pagination import MarketingDataPagination
from api.schemas import (
    MarketingDataSchema,
    MarketingDataFilterSchema,
    ChannelSalesPercentageSchema,
    ChannelWeeklySalesSchema,
)
from api.services.auth import generate_token
from api.services.marketing_measurements import get_marketing_data
from api.services.marketing_stats import (
    get_channel_sales_percentages,
    get_channel_weekly_sales,
)

ninja_api = NinjaAPI()

router = Router()


@router.get(
    "/measurements/",
    response={200: list[MarketingDataSchema], 401: dict, 400: dict},
    auth=AuthBearer(),
)
@paginate(MarketingDataPagination)
def marketing_measurements(
    request: HttpRequest, filters: MarketingDataFilterSchema = Query(None)
):
    data = get_marketing_data(filters.dict() if filters else {})
    return data


@router.get(
    "/stats/channel-sales-percentages/",
    response={200: list[ChannelSalesPercentageSchema], 401: dict, 400: dict},
    auth=AuthBearer(),
)
@paginate(MarketingDataPagination)
def channel_sales_percentages(
    request: HttpRequest,
    filters: MarketingDataFilterSchema = Query(None),
):
    data = get_channel_sales_percentages(filters.dict() if filters else {})
    return data


@router.get(
    "/stats/channel-weekly-sales/",
    response={200: list[ChannelWeeklySalesSchema], 401: dict, 400: dict},
    auth=AuthBearer(),
)
@paginate(MarketingDataPagination)
def channel_weekly_sales(
    request: HttpRequest, filters: MarketingDataFilterSchema = Query(None)
):
    data = get_channel_weekly_sales(filters.dict() if filters else {})
    return data


auth_router = Router()


@auth_router.get(
    "/token/",
    response={200: dict, 401: dict},
    auth=BasicAuth(),
)
def get_token(request: HttpRequest):
    user, password = BasicAuth().decode_authorization(request.headers["Authorization"])
    token = generate_token(user)

    return {"data": {"token": token}}


ninja_api.add_router("/marketing", router)
ninja_api.add_router("/auth", auth_router)
