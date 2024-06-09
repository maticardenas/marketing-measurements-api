from django.db.models import Q, Sum

from api.utils import calculate_percentage, build_filters_query
from core.models import Conversion


def get_channel_sales_percentages(
    filters: dict = {},
):
    initial_query = Q()

    if start_date := filters.get("start_date"):
        initial_query &= Q(date__gte=start_date)
    if end_date := filters.get("end_date"):
        initial_query &= Q(date__lte=end_date)

    total_conversion_in_period = (
        Conversion.objects.filter(initial_query).aggregate(total=Sum("conversions"))[
            "total"
        ]
        or 0
    )

    query = build_filters_query(**filters)

    channel_sales = (
        Conversion.objects.filter(query)
        .values("channel__name")
        .annotate(net_sales=Sum("conversions"))
        .order_by("-net_sales")
    )

    return [
        {
            "channel": channel_sale["channel__name"],
            "percentage": calculate_percentage(
                channel_sale["net_sales"], total_conversion_in_period
            ),
        }
        for channel_sale in channel_sales
    ]
