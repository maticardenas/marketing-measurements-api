from datetime import date

from django.db.models import Q


def calculate_percentage(value: float, total: float) -> float:
    try:
        return f"{((value / total) * 100):.2f}" if value > 0 else "0.00"
    except ZeroDivisionError:
        return "0.00"


def build_filters_query(
    products: list[str] = None,
    campaign_types: list[str] = None,
    channels: list[str] = None,
    campaigns: list[str] = None,
    start_date: date = None,
    end_date: date = None,
) -> Q:
    query = Q()

    if products:
        query &= Q(product__name__in=products)
    if campaign_types:
        query &= Q(campaign__campaign_type__name__in=campaign_types)
    if channels:
        query &= Q(channel__name__in=channels)
    if campaigns:
        query &= Q(campaign__name__in=campaigns)
    if start_date:
        query &= Q(date__gte=start_date)
    if end_date:
        query &= Q(date__lte=end_date)

    return query
