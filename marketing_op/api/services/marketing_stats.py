from django.db.models import Q, Sum
from django.db.models.functions import TruncWeek

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


def get_channel_weekly_sales(
    filters: dict = {},
):
    query = build_filters_query(**filters)

    conversions_grouped_by_week = (
        Conversion.objects.filter(query)
        .annotate(week=TruncWeek("date"))
        .values("week", "channel__name")
        .annotate(net_sales=Sum("conversions"))
        .order_by("week", "channel__name")
    )

    response_data = []
    for conversions in conversions_grouped_by_week:
        week_start_date = conversions["week"]
        year, week_number, _ = week_start_date.isocalendar()

        response_data.append(
            {
                "year": year,
                "week": week_number,
                "channel": conversions["channel__name"],
                "sales": conversions["net_sales"],
            }
        )

    return response_data
