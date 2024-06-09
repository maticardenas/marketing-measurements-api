from api.utils import build_filters_query
from core.models import Conversion


def get_marketing_data(
    filters: dict = {},
):
    query = build_filters_query(**filters)

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
