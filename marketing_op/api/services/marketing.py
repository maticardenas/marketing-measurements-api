from datetime import date

from django.db.models import Q

from core.models import Conversion


def get_marketing_data(
    products: list[str] = None,
    campaign_types: list[str] = None,
    channels: list[str] = None,
    campaigns: list[str] = None,
    start_date: date = None,
    end_date: date = None,
):
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

    # Retrieve the filtered conversions and include related objects
    marketing_data_conversions = Conversion.objects.filter(query).select_related(
        "campaign", "campaign__product", "campaign__campaign_type", "channel"
    )

    return [
        {
            "product": conversion.campaign.product.name,
            "campaign_type": conversion.campaign.campaign_type.name,
            "channel": conversion.channel.name,
            "campaign": conversion.campaign.name,
            "date": conversion.date,
            "conversions": conversion.conversions,
        }
        for conversion in marketing_data_conversions
    ]
