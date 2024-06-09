from django.http import HttpRequest
from ninja import NinjaAPI, Router, Query
from ninja.pagination import paginate

from api.pagination import MarketingDataPagination
from api.schemas import MarketingDataSchema, MarketingDataFilterSchema
from api.services.marketing import get_marketing_data

api = NinjaAPI()

router = Router()


@router.get(
    "/",
    response={200: list[MarketingDataSchema]},
)
@paginate(MarketingDataPagination)
def get_marketing_measurements(
    request: HttpRequest, filters: MarketingDataFilterSchema = Query(None)
):
    data = get_marketing_data(**filters.dict() if filters else {})
    return data


api.add_router("/marketing-measurements", router)
